from flask_jwt_extended import create_access_token
from flask_restful import Resource, request
from app.db import UserModel


class LoginResource(Resource):
    #json validator: {'username':type('string'), 'password':type('string')}
    def post(self):
        user = UserModel.query.filter_by(email=request.json['username']).first()
        if not user:
            return {'Error':'Usuario não encontrado!'}, 401   
        if not user.verify_password(request.json['password']):
            return {'Error':'Senha informada incorreta!'}, 401  
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token, 'username':user.username}, 200
