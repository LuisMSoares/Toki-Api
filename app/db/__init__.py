from flask_sqlalchemy import SQLAlchemy
bluep_db = SQLAlchemy()

from app.db.user import User
from app.db.subject import Subject, Subjectur
from app.db.absence import Absence, qtAbsence


def AddData(objdata):
    try:
        bluep_db.session.add(objdata)
        bluep_db.session.commit()
    except IntegrityError:
        bluep_db.session().rollback()
        return False
    return True


def DeleteData(objdata):
    bluep_db.session.delete(objdata)
    bluep_db.session.commit()
