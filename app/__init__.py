from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from os import environ
from app.db import db

app = Flask(__name__)


# Handling excetions
app.config['PROPAGATE_EXCEPTIONS'] = True
# ORM Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL','sqlite:///foo.db')
# JSON Web Token Configuration
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY', 'The quick brown fox jumps over the lazy dog')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False #timedelta(days=environ.get('JWT_EXPIRES_DAYS', 1))


# Database init
db.init_app(app)
# Flask Migrate
migrate = Migrate(app, db)
# JWT init
jwt = JWTManager(app)
# Api init
api = Api(app)
api.prefix = '/api'


from app.resource import (LoginResource, UserResource,
OwnerSubjectResource, AssociateSubjectResource,
AbsenceResource, ValidateAbsenceResource)

api.add_resource(UserResource, '/user') #ok
api.add_resource(LoginResource, '/login') #ok
api.add_resource(OwnerSubjectResource, '/subject', '/subject/<int:subject_id>')
api.add_resource(AssociateSubjectResource, '/subject/associate')
api.add_resource(AbsenceResource, '/absence')
api.add_resource(ValidateAbsenceResource, '/absence/validate') #ok


# Status code routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404


# Create database tables
with app.app_context():
    # remove this in production - start remove
    #db.drop_all()
    #print(' * Drop all tables!')
    # end remove
    db.create_all()