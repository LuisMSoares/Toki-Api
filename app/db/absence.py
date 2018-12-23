from app.db import bluep_db as db
from app.db import User, Subject
import datetime


class Absence(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    device_id = db.Column(db.String(120), nullable=False)

    def __init__(self, subject_id, user_id, vdate, device_id):
        self.subject_id = subject_id
        self.user_id = user_id
        year, month, day = vdate.split('-')# vdate = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))
        self.device_id = device_id

    def todict(self):
        keys = ['id', 'subject_id', 'user_id', 'date', 'device_id']
        values = [self.id, self.subject_id, self.user_id, self.date, self.device_id]
        return dict(zip(keys,values))

    __table_args__ = (
        db.Index('duplicated_device1', subject_id, device_id, user_id, date, unique=True),
        db.Index('duplicated_device2', subject_id, device_id, date, unique=True),
        db.Index('duplicated_validated', subject_id, user_id, date, unique=True),
    )


class qtAbsence(db.Model):
    __tablename__ = 'qtpresencas'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, subject_id, vdate):
        self.subject_id = subject_id
        year, month, day = vdate.split('-')# vdate = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))
    
    __table_args__ = (
        db.Index('only_qtabsence', subject_id, date, unique=True),
    )
