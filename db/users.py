from app import db

class Users(db.Model):
    __tablename__ = 'usuarios'

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
