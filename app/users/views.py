from . import users
from .. import db
from ..models import *
from flask import session, redirect, request, render_template, send_from_directory, Response
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import json
import os
import shutil
import time


def comm_all(num):
    # comm = Comment.query.all()
    comm = db.session.query(Comment).order_by('id desc').limit(20).offset(num).all()
    lst = []
    for c in comm:
        dic = c.to_dict()
        lst.append(dic)
    return lst


# 使用文件流传输
def send_file(filepath):
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(10*1024*1024)
            if not data:
                break
            yield data


def c_time(bpath, lst):
    create_time = []
    for f in lst:
        ct = os.path.getctime(os.path.join(bpath, f))
        create_time.append(ct)
    return create_time


# 获取文件名以及文件相关信息打包成一个列表套字典
def make_data(bpath, lst):
    data = []
    for f in lst:
        ct = time.localtime(os.path.getctime(os.path.join(bpath, f)))  # 转换为当地时间
        dic = {
            'fname': f,
            'ctime': time.strftime('%Y年%m月%d日 %H:%M:%S', ct)
        }
        data.append(dic)
    return data



@users.route('/logout')
def logout_view():
    resp = redirect('/')
    if 'uname' in session:
        del session['uname']
    if 'uname' in request.cookies:
        resp.delete_cookie('uname')
    return resp


@users.route('/get_comm')
def get_comm_view():
    num = session['pnum']
    lst = comm_all(num)
    lst = json.dumps(lst)
    return lst


@users.route('/next_page')
def next_page_view():
    all_page = db.session.query(Comment).count()
    if request.args['statu'] == 'pos' and session['pnum'] < all_page:
        session['pnum'] += 20
        return json.dumps(1)
    elif request.args['statu'] == 'ngtv':
        if session['pnum'] > 0:
            session['pnum'] -= 20
            return json.dumps(1)
        return json.dumps(0)
    else:
        return json.dumps(2)


@users.route('/history')
def get_history():
    uname = session['uname']
    user = User.query.filter_by(uname=uname).first()
    upwd = session['password']
    if user and check_password_hash(user.upwd, upwd):
        #执行后端业务
        lst = []
        comms = user.comments
        for c in comms:
            dic = c.to_dict()
            lst.append(dic)
        return json.dumps(lst)
    else:
        return redirect('/')


@users.route('/del_record')
def delete_record():
    cid = request.args['cid']
    comm = Comment.query.filter_by(id=cid).first()
    user = comm.user.uname
    if 'uname' in session and user == session['uname']:
        if comm.image:
            # 完成删除文章时,连带用户图片从本机中删除
            path = os.path.dirname(os.path.dirname(__file__)) + '/static/'
            path = os.path.join(path, comm.image)
            os.remove(path)
        anws = comm.answers
        for a in anws:
            db.session.delete(a)
        db.session.delete(comm)
        return json.dumps(1)
    return json.dumps(0)


@users.route('/answer', methods=["POST"])
def answer_views():
    anw = request.form['anw']
    print(anw)
    cid = request.form['cid']
    uid = User.query.filter_by(uname=session['uname']).first().id
    answer = Answer(anw, cid, uid)
    db.session.add(answer)
    return json.dumps(1)


@users.route('/show_answer')
def show_answer():
    cid = request.args['cid']
    anws = Answer.query.filter_by(cid=cid).all()
    if not anws:
        return json.dumps(0)
    lst = []
    for a in anws:
        lst.append(a.to_dic())
    return json.dumps(lst)


@users.route('/islog')
def islog():
    if 'uname' in session:
        return json.dumps(1)
    else:
        return json.dumps(0)


@users.route('/skydisk')
def skydisk():
    if 'index' not in request.args:
        # lst = os.listdir(session['upath'])
        abs_path = session['upath']
        lst = make_data(abs_path, os.listdir(session['upath']))
        # create_time = os.path.getctime(abs_path)
        session['upath'] = abs_path
        uroot = '/'
        return render_template('Skydisk.html', dirlist=locals())
    else:
        index = request.args['index']
        frot = index.split('/')[0:-1]
        frot_path = '/'+'/'.join(frot)
        filename = index.split('/')[-1]
        uroot = index.split('/')[9:]
        uroot = '/' + '/'.join(uroot)
        if os.path.isfile(index):
            response = Response(send_file(index), content_type='application/octet-stream')
            response.headers['Content-disposition'] = 'attachment; filename=%s' % filename.encode().decode('latin-1')
            response.headers['Content-Length'] = os.path.getsize(index)
            print('已发送请求1')
            return response
            # return send_from_directory(frot_path, filename, as_attachment=True)
        # lst = os.listdir(index)
        abs_path = index
        lst = make_data(abs_path, os.listdir(index))
        # create_time = c_time(abs_path, lst)
        return render_template('Skydisk.html', dirlist=locals())


@users.route('/makefile')
def makefile():
    if request.args['flag'] == 'mkdir':
        dirName = request.args['dirName']
        upath = request.args['abs_path']
        newpath = os.path.join(upath, dirName)
        if os.path.exists(newpath):
            return json.dumps(0)
        os.mkdir(newpath)
        return json.dumps(1)
    elif request.args['flag'] == 'remove':
        dirName = request.args['delfile']
        upath = request.args['abs_path']
        delpath = os.path.join(upath, dirName)
        print(delpath)
        if not os.path.exists(delpath):
            return json.dumps(0)
        shutil.rmtree(delpath)
        return json.dumps(1)


@users.route('/push_file', methods=["POST"])
def topath():
    path = request.form['path']
    abs_path = path
    lst = make_data(abs_path, os.listdir(path))
    # create_time = c_time(abs_path, lst)
    f = request.files['file']
    # lst = os.listdir(path)
    uroot = path.split('/')[9:]
    uroot = '/' + '/'.join(uroot)
    fname = f.filename
    save_path = os.path.join(path, fname)
    f.save(save_path)
    # return render_template('Skydisk.html', dirlist=locals())
    return json.dumps(1)


@users.route('/delfiles', methods=["POST"])
def delfile():
    now_dir = request.form['now_path']
    len_lst = len(os.listdir(now_dir))
    for n in range(len_lst):
        d_id = 'del'+str(n)
        if d_id in request.form:
            f = request.form[d_id]
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
    uroot = '/'+'/'.join(now_dir.split('/')[9:])
    # lst = os.listdir(now_dir)
    abs_path = now_dir
    lst = make_data(abs_path, os.listdir(now_dir))
    # create_time = c_time(abs_path, lst)
    # return render_template('Skydisk.html', dirlist=locals())
    return json.dumps(1)

























