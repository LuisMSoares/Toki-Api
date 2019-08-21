from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


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
    #db.drop_all()
    #print(' * Drop all tables!')
    # end remove
    db.create_all()