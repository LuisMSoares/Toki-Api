from app.db import bluep_db as db


class User(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    enrolment = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, username, password, enrolment, email):
        self.username = username
        self.password = password
        self.enrolment = enrolment
        self.email = email
