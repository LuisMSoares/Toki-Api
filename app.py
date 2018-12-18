from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgresql/projectdb'
db = SQLAlchemy(app)

from db.tables import User, Subject, Absence

def dbcommit(obj):
    db.session.add(obj)
    db.session.commit()


@app.route('/')
def index():
    try:
        db.session.add(User(username='Luis Eduardo', 
            password='1234', enrolment='0000', email='Luis@Luis'))
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
    dbcommit( Subject(user_id=1, subname='Teste Disciplina', subgroup=1337) )
    dbcommit( Absence(subject_id=1, user_id=1, sdate='2018-12-14') )
    return 'Commit data'


@app.route('/reguser', methods=['POST'])
def register():
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


@app.route('/listsubject', methods=['GET'])
def listsbject():
    auth = request.authorization
    user_id = (userauth(auth.username,auth.password)).id
    disci = Subject.query.filter_by(user_id=user_id).all()
    db.session.commit()
    values = [row.todict() for row in disci]
    return jsonify({'values':f'{values}'}), 200


def userauth(username,password):
    user = User.query.filter_by(email=username,password=password).first()
    db.session.commit()
    if not user:
        return False
    if user.password == password:
        return user
    return False


def recreate_db():
    from db import db
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(' * Recreating Database')
if __name__ == '__main__':
    recreate_db() # comment this line to deactivate
    app.run(host='0.0.0.0',debug=True)
