from app.db import bluep_db as db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    enrolment = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, username, password, enrolment, email):
        self.username = username
        self.hash_password(password)
        self.enrolment = enrolment
        self.email = email

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password) # return True or False