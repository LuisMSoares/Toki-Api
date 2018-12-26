from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.db import bluep_db

app = Flask(__name__)


# Database config

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgresql/projectdb'
bluep_db.init_app(app)
with app.app_context():
    # remove this in production - start remove
    from sqlalchemy.exc import OperationalError
    try:
        #bluep_db.drop_all()
        print(' * Drop all tables!')
    except OperationalError:
        pass
    # end remove
    bluep_db.create_all()


# Routes blueprints

#  absence route
from app.routes.rabsence import abapp
app.register_blueprint(abapp)
#  subject route
from app.routes.rsubject import sapp
app.register_blueprint(sapp)
#  user route
from app.routes.ruser import uapp
app.register_blueprint(uapp)
#  validade absence route
from app.routes.rvabsence import abvapp
app.register_blueprint(abvapp)


# Status code routes

@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404