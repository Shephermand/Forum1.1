from . import users
from .. import db
from ..models import *
from flask import session, redirect, request, render_template
from werkzeug.security import check_password_hash
import json
import os
import shutil


def comm_all(num):
    # comm = Comment.query.all()
    comm = db.session.query(Comment).order_by('id desc').limit(20).offset(num).all()
    lst = []
    for c in comm:
        dic = c.to_dict()
        lst.append(dic)
    return lst


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
    lst = os.listdir(session['upath'])
    if 'index' not in request.args:
        session['seek'] = session['upath']
        print(lst)
        path = session['seek']
        return render_template('Skydisk.html', dirlist=locals())
    else:
        index = request.args['index']
        path = os.path.join(session['seek'], lst[int(index)])
        session['seek'] = path
        lst = os.listdir(path)
        return render_template('Skydisk.html', dirlist=locals())


@users.route('/makefile')
def makefile():
    if request.args['flag'] == 'mkdir':
        dirName = request.args['dirName']
        upath = session['seek']
        newpath = os.path.join(upath, dirName)
        if os.path.exists(newpath):
            return json.dumps(0)
        os.mkdir(newpath)
        return json.dumps(1)
    elif request.args['flag'] == 'remove':
        dirName = request.args['delfile']
        upath = session['seek']
        delpath = os.path.join(upath, dirName)
        print(delpath)
        if not os.path.exists(delpath):
            return json.dumps(0)
        shutil.rmtree(delpath)
        return json.dumps(1)


@users.route('/topath')
def topath():
    return json.dumps()


















