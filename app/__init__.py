from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.db import bluep_db

app = Flask(__name__)


# Database config

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgresql/projectdb'
bluep_db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'The quick brown fox jumps over the lazy dog'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)



# Routes blueprints

#  user route
from app.routes.user import uapp
app.register_blueprint(uapp, url_prefix='/user')
#  subject route
from app.routes.subject import sapp
app.register_blueprint(sapp, url_prefix='/subject')
#  absence route
from app.routes.absence import abapp
app.register_blueprint(abapp, url_prefix='/absence')
#  validade absence route
from app.routes.vabsence import abvapp
app.register_blueprint(abvapp, url_prefix='/absence')


# Status code routes

@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404


# Create database tables

with app.app_context():
    # remove this in production - start remove
    #bluep_db.drop_all()
    #print(' * Drop all tables!')
    # end remove
    bluep_db.create_all()