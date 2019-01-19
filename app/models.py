from . import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), unique=True)
    upwd = db.Column(db.String(300))
    nickname = db.Column(db.String(50))

    comments = db.relationship(
        "Comment",
        backref='user',
        lazy='dynamic'
    )

    replies = db.relationship(
        "Reply",
        backref='user',
        lazy='dynamic'
    )

    answers = db.relationship(
        "Answer",
        backref="user",
        lazy="dynamic"
    )

    def __init__(self, uname, upwd, nickname):
        self.uname = uname
        self.upwd = upwd
        self.nickname = nickname


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    image = db.Column(db.Text)
    up_time = db.Column(db.TIMESTAMP, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    answers = db.relationship(
        "Answer",
        backref='comm',
        lazy='dynamic'
    )

    def __init__(self, text, uid):
        self.text = text
        self.uid = uid


    def to_dict(self):
        dic = {
            'cid':self.id,
            'uname': self.user.uname,
            'uid': self.uid,
            'text': self.text,
            'up_time': str(self.up_time),
            'nickname': self.user.nickname,
            'image': self.image,
        }
        return dic


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    anw = db.Column(db.String(150), nullable=False)
    a_time = db.Column(db.TIMESTAMP, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('comment.id'))
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    replies = db.relationship(
        'Reply',
        backref='answer',
        lazy='dynamic'
    )

    def __init__(self, anw, cid, uid):
        self.anw = anw
        self.cid = cid
        self.uid = uid

    def to_dic(self):
        dic = {
            'id': self.id,
            'anw': self.anw,
            'a_time': str(self.a_time),
            'uname': self.user.nickname
        }
        return dic


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    rpl = db.Column(db.String(150), nullable=False)
    r_time = db.Column(db.TIMESTAMP, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    aid = db.Column(db.Integer, db.ForeignKey('answer.id'))




