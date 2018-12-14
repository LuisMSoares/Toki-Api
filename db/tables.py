from app import db

import datetime

class User(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    enrolment = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, enrolment, email):
        self.username = username
        self.password = password
        self.enrolment = enrolment
        self.email = email

class Subject(db.Model):
    __tablename__ = 'disciplina'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    subname = db.Column(db.String(80), nullable=False)
    subgroup = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, subname, subgroup):
        self.user_id = user_id
        self.subname = subname
        self.subgroup = subgroup

class Absence(db.Model):
    __tablename__ = 'falta'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, subject_id, user_id, sdate):
        self.subject_id = subject_id
        self.user_id = user_id
        year, month, day = sdate.split('-')# sdate = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))

