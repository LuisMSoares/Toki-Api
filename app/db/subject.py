from app.db import bluep_db as db
from app.db import User, Absence, Presence


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String, nullable=False)
    sub_group = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user_associated = db.relationship('Subuser', backref='subj_associate')
    presence_count = db.relationship('Presence', backref='subject_info')

    def __init__(self, sub_name, sub_group, creator):
        self.sub_name = user_id
        self.sub_group = subname
        self.creator = creator


class Subuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    absences = db.relationship('Absence', backref='user_absence')

    def __init__(self, subj_associate, user_associate):
        self.subj_associate = subj_associate
        self.user_associate = user_associate

    __table_args__ = (
        db.Index('only_subuser', sub_id, user_id, unique=True),
    )