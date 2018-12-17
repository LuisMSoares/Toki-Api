from flask_httpauth import HTTPBasicAuth
from flask import request, make_response, jsonify
from app import db
from db.tables import User

auth = HTTPBasicAuth()

'''
> autenticação: retorne o usuario pelo endereço de email, e com o objeto em memoria, compare as senhas
se for igual retorne a autencicação com sucesso, caso contrario aborte e exiba uma mensagem de erro de
senha invalida.

'''


@auth.verify_password
def get_pw(username,password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    if user.password == password:
        return True
    return False
    


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)