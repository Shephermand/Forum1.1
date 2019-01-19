from flask import Blueprint
users = Blueprint('users', __name__)
from . import views


def ansysize(size):
    if size == 0:
        return "目录"
    elif size < 1024:
        return str(size)+'B'
    elif 1024 < size < pow(1024, 2):
        anw = round(size/1024, 2)
        s = str(anw)+'KB'
    elif pow(1024, 2) < size < pow(1024, 3):
        anw = round(size/pow(1024, 2))
        s = str(anw) + 'MB'
    else:
        anw = round(size/pow(1024, 3))
        s = str(anw) + 'GB'
    return s

users.add_app_template_filter(ansysize, 'humsize')

