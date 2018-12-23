from flask_sqlalchemy import SQLAlchemy
bluep_db = SQLAlchemy()

from app.db.user import User
from app.db.subject import Subject, Subjectur
from app.db.absence import Absence, qtAbsence