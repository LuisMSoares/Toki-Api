from app.db import bluep_db as db
from app.db import User, Subject
import datetime


class Absence(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, subject_id, user_id, vdate):
        self.subject_id = subject_id
        self.user_id = user_id
        year, month, day = vdate.split('-')# vdate = year-month-day -> 2018-12-14
        self.date = datetime.date(int(year), int(month), int(day))

    def todict(self):
        keys = ['id', 'subject_id', 'user_id', 'date']
        values = [self.id, self.subject_id, self.user_id, self.date]
        return dict(zip(keys,values))


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
        db.Index('only_absence', subject_id, date, unique=True),
    )
