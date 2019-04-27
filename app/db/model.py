from app.db import bluep_db as db
from passlib.apps import custom_app_context as pwd_context
import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    enrolment = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)

    subj_associated = db.relationship('Subuser', backref='user_associate')
    my_subject = db.relationship('Subject', backref='creator')

    def __init__(self, username, password, enrolment, email):
        self.username = username
        self.hash_password(password)
        self.enrolment = enrolment
        self.email = email

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password) # return True or False


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String, nullable=False)
    sub_group = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user_associated = db.relationship('Subuser', backref='subj_associate', passive_deletes=True)
    presence_count = db.relationship('Presence', backref='subject_info', passive_deletes=True)

    def __init__(self, sub_name, sub_group, creator):
        self.sub_name = sub_name
        self.sub_group = sub_group
        self.creator = creator


class Subuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    absences = db.relationship('Absence', backref='user_absence', passive_deletes=True, order_by='Absence.date')

    __table_args__ = (
        db.Index('only_subuser', sub_id, user_id, unique=True),
    )


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    usubj_id = db.Column(db.Integer, db.ForeignKey('subuser.id', ondelete="CASCADE"))
    dup_security = db.Column(db.Integer, nullable=False)

    def __init__(self, date, user_absence, device_id, dup_security):
        year, month, day = date.split('-')# date = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))
        self.user_absence = user_absence
        self.device_id = device_id
        self.dup_security = dup_security
    
    def PresenceCount(self, sub_id):
        return Presence(sub_id=sub_id ,date=self.date)
    
    __table_args__ = (
        db.Index('duplicated_device', dup_security, device_id, date, unique=True),
        db.Index('already_registred', usubj_id, date, unique=True),
    )


class Presence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"))
    date = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.Index('unique_count', sub_id, date, unique=True),
    )