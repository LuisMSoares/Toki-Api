from flask import Blueprint, request, jsonify
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError #incluir exception dataerror
from app.db import User, Absence, qtAbsence, Subject
from app.db import bluep_db as db

mapp = Blueprint('mapp',__name__)


@mapp.route('/')
def index():
    return 'ola'


def userauth(username,password):
    user = User.query.filter_by(email=username,password=password).first()
    if not user:
        return False
    if user.password == password:
        return user
    return False


@mapp.route('/reguser', methods=['POST'])
def reguser():
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


@mapp.route('/listsubject', methods=['GET'])
def listsubject():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    disci = Subject.query.filter_by(user_id=user.id).all()
    values = [row.todict() for row in disci]
    if len(values) == 0:
        return jsonify({'Error':'Nenhuma disciplina cadastrada pelo usuario foi encontrada'}), 200
    data = {}
    data['values'] = values
    return jsonify(data), 200


@mapp.route('/regsubject', methods=['POST'])
def regsubject():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rjson = request.json
    subject = Subject(user_id=user.id,
                      subname=rjson['sname'],
                      subgroup=rjson['sgroup'])
    try:
        db.session.add(subject)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        return jsonify({'Error': 'Ocorreu algum erro ao tentar realizar o cadastro!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@mapp.route('/absence/validade', methods=['POST'])
def abvalidade():
    rjson = request.json
    absence = Absence(subject_id=rjson['subjid'],
                      user_id=rjson['userid'],
                      vdate=rjson['vdate'],
                      device_id=rjson['dvcid'])
    qtabsence = qtAbsence(subject_id=rjson['subjid'],
                          vdate=rjson['vdate'])
    try:
        try:
            db.session.add(qtabsence)
            db.session.commit()
        except IntegrityError:
            db.session().rollback()
        db.session.add(absence)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        absences = Absence.query.filter_by(device_id=rjson['dvcid']).all()
        for row in absences:
            db.session.delete(row)
        db.session.commit()
        return jsonify({'Success': 'Dispositivos duplicados detectados'}), 201
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@mapp.route('/subject/relation', methods=['GET'])
def relationsub():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rjson = request.json
    #select distinct subject_id from presencas where user_id=1
    