from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.db.model import *


def AddData(objdata):
    try:
        bluep_db.session.add(objdata)
        bluep_db.session.commit()
    except:
        bluep_db.session().rollback()
        return False
    return True


def DeleteData(objdata):
    try:
        bluep_db.session.delete(objdata)
        bluep_db.session.commit()
    except:
        bluep_db.session().rollback()
        return False
    return True
