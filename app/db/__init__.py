from flask_sqlalchemy import SQLAlchemy
bluep_db = SQLAlchemy()

from app.db.user import User
from app.db.subject import Subject
from app.db.absence import Absence
from app.db.absence import qtAbsence