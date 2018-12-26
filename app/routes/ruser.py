from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db import User
from app.db import bluep_db as db

uapp = Blueprint('ruser',__name__)



@uapp.route('/reguser', methods=['POST'])
def reguser():
    rjson = request.json
    user = User(username=rjson['uname'],
                password=rjson['passw'],
                enrolment=rjson['enrol'],
                email=rjson['email'])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        return jsonify({'Error': 'Já existe um usuario cadastrado com esta matricula ou email!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201
