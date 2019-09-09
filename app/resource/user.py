from flask_restful import Resource, request
from app.db import UserModel, AddData


class UserResource(Resource):
    #json validator: {'uname':type('string'), 'passw':type('string'), 'enrol':type('string'), 'email':type('string')}
    def post(self):
        user = UserModel(username=request.json['uname'],
                    password=request.json['passw'],
                    enrolment=request.json['enrol'],
                    email=request.json['email'])
        if not AddData(user):
            return {'Error' : 'Já existe um usuario cadastrado com esta matricula ou email!'}, 500
        return {'Success' : 'Registro realizado com sucesso'}, 201