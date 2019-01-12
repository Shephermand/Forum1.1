from . import users
from .. import db
from ..models import *
from flask import session, redirect, request
from werkzeug.security import check_password_hash
import json
import os


def comm_all():
    # comm = Comment.query.all()
    comm = db.session.query(Comment).order_by('id desc').limit(20)
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
    lst = comm_all()
    lst = json.dumps(lst)
    return lst


@users.route('/history')
def get_history():
    uname = session['uname']
    user = User.query.filter_by(uname=uname).first()
    upwd = session['password']
    if user and check_password_hash(user.upwd,upwd):
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
        # 完成删除文章时,连带用户图片从本机中删除
        path = os.path.dirname(os.path.dirname(__file__)) + '/static/'
        path = os.path.join(path, comm.image)
        os.remove(path)
        db.session.delete(comm)
        return json.dumps(1)
    return json.dumps(0)


@users.route('/answer', methods=["POST"])
def answer_views():
    anw = request.form['anw']
    print(anw)
    cid = request.form['cid']
    uid = request.form['uid']
    answer = Answer(anw, cid, uid)
    db.session.add(answer)
    return json.dumps(1)


@users.route('/show_answer')
def show_answer():
    cid = request.args['cid']
    anws = Answer.query.filter_by(cid=cid).all()
    if not anws:
        print('空!')
        return json.dumps(0)
    lst = []
    for a in anws:
        lst.append(a.to_dic())
    return json.dumps(lst)



