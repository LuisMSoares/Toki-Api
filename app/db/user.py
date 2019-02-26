from app.db import bluep_db as db
from app.db import Subject, Subuser
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
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
