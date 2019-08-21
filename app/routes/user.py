from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.db import *
from app.routes import json_verification

uapp = Blueprint('ruser',__name__)


""" @uapp.route('/register', methods=['POST'])
def reguser():
    keys, rjson = ['uname','passw','enrol','email'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    user = User(username=rjson['uname'],
                password=rjson['passw'],
                enrolment=rjson['enrol'],
                email=rjson['email']
    )
    if not AddData(user):
        return jsonify({'Error': 'Já existe um usuario cadastrado com esta matricula ou email!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@uapp.route('/login', methods=['POST'])
def loguser():
    keys, rjson = ['username','password'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    user = User.query.filter_by(email=rjson['username']).first()
    if not user:
        return jsonify({'Error':'Usuario não encontrado!'}), 401   
    if not user.verify_password(rjson['password']):
        return jsonify({'Error':'Senha informada incorreta!'}), 401  
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'username':user.username}), 200 """