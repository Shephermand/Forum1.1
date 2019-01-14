from . import main
from .. import db
from ..models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template, redirect, session
import os
import datetime
import http.client
import hashlib
from urllib import parse
import random


# @main.route('/')
# def index():
#     if "uname" in session:
#         uname = session.get('uname')
#         user = User.query.filter_by(uname=uname).first()
#     return render_template('100-main.html',params=locals())


def create_space():
    base_path = os.path.dirname(os.path.dirname(__file__))
    sec_path = os.path.join(base_path, 'static/Skydisk')
    path = os.path.join(sec_path, session['uname'])
    if not os.path.exists(path):
        os.mkdir(path)
    return None


@main.route('/register', methods=["GET", "POST"])
def register_view():
    if request.method == "GET":
        return render_template('register.html')
    else:
        uname = request.form['uname']
        upwd = request.form['upwd']
        upwd = generate_password_hash(upwd)
        nickname = request.form['nickname']
        user = User(uname,upwd,nickname)
        # print(user.uname)
        db.session.add(user)
        session['uname'] = uname
        session['password'] = upwd
        session['pnum'] = 0
        return redirect('/My_page')


@main.route('/check')
def check_view():
    uname = request.args['uname']
    user = User.query.filter_by(uname=uname).first()
    if not user:
        return '0'
    else:
        return '1'


@main.route('/login', methods=["GET", "POST"])
def login_view():
    if request.method == "GET":
        url = request.headers.get('Referer', '/')
        session['url'] = url

        if 'uname' in session:
            # return redirect(url)
            user = User.query.filter_by(uname=session['uname']).first()
            return render_template('My_page.html', nickname=user.nickname)
        else:
            if 'uname' in request.cookies:
                uname = request.cookies['uname']
                user = User.query.filter_by(uname=uname).first()
                if user:
                    session['uname'] = uname
                    return redirect(url)
            return render_template('login.html')
    else:
        uname = request.form['uname']
        upwd = request.form['upwd']
        user = User.query.filter_by(uname=uname).first()
        if user and check_password_hash(user.upwd, upwd):
            session['uname'] = uname
            session['password'] = upwd
            session['pnum'] = 0
            # url = session.get('url','/')
            url = '/My_page'
            resp = redirect(url)

            if 'isSaved' in request.form:
                resp.set_cookie('uname', uname, 60*60*24*365*10)

            return resp
        else:
            return render_template('login.html', errMsg='用户名或密码不正确')


@main.route('/My_page', methods=["GET", "POST"])
def My_page_view():
    if request.method == "GET":
        if 'uname' in session:
            create_space()
            user = User.query.filter_by(uname=session['uname']).first()
            comm = Comment.query.all()
            return render_template('My_page.html', nickname=user.nickname)
        else:
            return redirect('/')
    else:
        uname = session['uname']
        text = request.form['uinfo']
        user = User.query.filter_by(uname=uname).first()
        uid = user.id
        comment = Comment(text, uid)
        if request.files:
            f = request.files['image']
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%S%M%f")
            ext = f.filename.split('.')[1]
            filename = ftime + '.' + ext
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir, 'static/upload_image', filename)
            f.save(upload_path)
            comment.image = "upload_image/" + filename
        db.session.add(comment)
        return render_template('My_page.html', nickname=user.nickname)


@main.route('/', methods=['GET', 'POST'])
def main_views():
    if request.method=='GET':

        return render_template('100-main.html')
    else:
        # neirong=request.form['check']

        if not request.form['check']:
            return render_template('100-main.html')
        appid = '20190101000253821'
        secretKey = 'cUwc4sxU3fPbN1gGJ4WK'
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q = request.form['check']
        print(q)
        print(request.form['langv'])
        fromLang = 'auto'
        toLang = request.form['langv']
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' \
                + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            str1 = response.read().decode('utf-8')
            str1 = eval(str1)
            line = str1['trans_result'][0]
            print("line:",line)
            print(line['dst'])
            # print(s)
            src=line['src']
            dst=line['dst']
            return render_template('100-main.html',dst=dst,src=src)
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
