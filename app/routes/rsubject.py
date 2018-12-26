from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db import Subject, Subjectur
from app.db import bluep_db as db
from app.routes import userauth

sapp = Blueprint('rsubject',__name__)



@sapp.route('/listsubject', methods=['GET'])
def listsubject():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    disci = Subject.query.filter_by(user_id=user.id).all()
    values = [row.todict() for row in disci]
    if len(values) == 0:
        return jsonify({'Error':'Nenhuma disciplina cadastrada pelo usuario foi encontrada'}), 404
    data = {}
    data['values'] = values
    return jsonify(data), 200


@sapp.route('/regsubject', methods=['POST'])
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



@sapp.route('/subject/relation', methods=['GET'])
def relationsub():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rabsence = Subjectur.query.filter_by(user_id=user.id)
    if rabsence.count() == 0:
        return jsonify({'Error':'Nenhuma disciplina relacionada ao usuario foi encontrada'}), 404
    subids = [row.subj_id for row in rabsence]
    disci = Subject.query.filter(Subject.id.in_(subids))
    values = [row.todict() for row in disci]
    data = {}
    data['values'] = values
    return jsonify(data), 200
