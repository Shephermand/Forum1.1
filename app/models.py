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

    def __init__(self, uname, upwd, nickname):
        self.uname = uname
        self.upwd = upwd
        self.nickname = nickname

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    up_time = db.Column(db.TIMESTAMP, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, text, uid):
        self.text = text
        self.uid = uid

    def to_dict(self):
        dic = {
            'uname': self.user.uname,
            'text': self.text,
            'up_time': str(self.up_time),
        }
        return dic
