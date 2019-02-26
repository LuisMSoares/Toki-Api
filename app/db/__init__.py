from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

bluep_db = SQLAlchemy()


from app.db.model import User, Subject, Subuser, Absence, Presence


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
