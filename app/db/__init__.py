from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.db.model import UserModel, SubjectModel, SubuserModel, AbsenceModel, PresenceModel


def AddData(objdata):
    try:
        db.session.add(objdata)
        db.session.commit()
    except:
        db.session().rollback()
        return False
    return True


def DeleteData(objdata):
    try:
        db.session.delete(objdata)
        db.session.commit()
    except:
        db.session().rollback()
        return False
    return True
