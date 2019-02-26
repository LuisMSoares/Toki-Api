from app.db import bluep_db as db
from app.db import Subject, Subuser
import datetime


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    usubj_id = db.Column(db.Integer, db.ForeignKey('subuser.user_id'))

    def __init__(self, date, user_absence):
        year, month, day = vdate.split('-')# vdate = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))
        self.user_absence = user_absence
    
    def PresenceCount(self, subject):
        return Presence(subject_info=subject ,date=self.date)
    
    __table_args__ = (
        db.Index('duplicated_device', usubj_id, device_id, date, unique=True),
        db.Index('already_registred', usubj_id, date, unique=True),
    )


class Presence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    date = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.Index('unique_count', sub_id, date, unique=True),
    )