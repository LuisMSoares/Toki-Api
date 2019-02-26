from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    subj_associated = db.relationship('Subuser', backref='user_associate')
    my_subject = db.relationship('Subject', backref='creator')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String, nullable=False)
    sub_group = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user_associated = db.relationship('Subuser', backref='subj_associate')
    presence_count = db.relationship('Presence', backref='subject_info')


class Subuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    absences = db.relationship('Absence', backref='user_absence')


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    #device_id = db.Column(db.String(80))
    usubj_id = db.Column(db.Integer, db.ForeignKey('subuser.user_id'))


class Presence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    date = db.Column(db.String(20), nullable=False)


#------------------------------------------------------------------------------

def add(object):
    db.session.add(object)
    db.session.commit()


def recreate():
    try:
        db.drop_all()
        db.create_all()
    except Exception:
        pass

def main():
    try:
        db.drop_all()
        db.create_all()
    except Exception:
        pass

    u1 = User(username='João', password='test1', email='test1@test')
    u2 = User(username='Jose', password='test2', email='test2@test')

    add(u1)
    add(u2)

    s1 = Subject(sub_name='Materia 1', sub_group='1', creator=u1)
    s2 = Subject(sub_name='Materia 2', sub_group='2', creator=u2)

    add(s1)
    add(s2)

    sr1 = Subuser(subj_associate=s1 ,user_associate=u1)
    sr2 = Subuser(subj_associate=s2 ,user_associate=u1)
    sr3 = Subuser(subj_associate=s1 ,user_associate=u2)

    add(sr1)
    add(sr2)
    add(sr3)

    ab1 = Absence(date='20/02/19', user_absence=sr1)
    ab2 = Absence(date='21/02/19', user_absence=sr2)
    ab3 = Absence(date='22/02/19', user_absence=sr3)
    
    add(ab1)
    add(ab2)
    add(ab3)
    
    p1 = Presence(subject_info=s1 ,date='20/02/19')
    p2 = Presence(subject_info=s1 ,date='21/02/19')
    p3 = Presence(subject_info=s2 ,date='22/02/19')

    add(p1)
    add(p2)
    add(p3)


#    __table_args__ = (
#        db.Index('duplicated_device1', subject_id, device_id, user_id, date, unique=True),
#        db.Index('duplicated_device2', subject_id, device_id, date, unique=True),
#    )