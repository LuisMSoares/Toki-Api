from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.db import bluep_db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgresql/projectdb'
bluep_db.init_app(app)
with app.app_context():
    bluep_db.drop_all()
    bluep_db.create_all()

from app.routes.mapp import mapp
app.register_blueprint(mapp)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
