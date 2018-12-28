from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.db import User
from app.db import bluep_db as db
from app.routes import userauth
from passlib.apps import custom_app_context as pwd_context

uapp = Blueprint('ruser',__name__)


@uapp.route('/register', methods=['POST'])
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


@uapp.route('/login', methods=['POST'])
def loguser():
    rjson = request.json
    user = User.query.filter_by(email=rjson['username']).first()
    if not user:
        return jsonify({'Error':'Usuario não encontrado!'}), 401   
    if user.verify_password(rjson['password']):
        return jsonify({'Error':'Senha informada incorreta!'}), 401  
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200