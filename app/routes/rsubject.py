from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db import Subject, Subjectur, qtAbsence, Absence
from app.db import AddData
from flask_jwt_extended import ( jwt_required, get_jwt_identity )

sapp = Blueprint('rsubject',__name__)


@sapp.route('/register', methods=['POST'])
@jwt_required
def regsubject():
    userid = get_jwt_identity()
    rjson = request.json
    subject = Subject(user_id=userid,
                      subname=rjson['sname'],
                      subgroup=rjson['sgroup'])
    if not AddData(subject):
        return jsonify({'Error': 'Ocorreu algum erro ao tentar realizar o cadastro!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@sapp.route('/enrolled/all', methods=['GET'])
@jwt_required
def relationsub():
    userid = get_jwt_identity()
    rabsence = Subjectur.query.filter_by(user_id=userid)
    if rabsence.count() == 0:
        return jsonify({'Error':'Nenhuma disciplina relacionada ao usuario foi encontrada'}), 404
    subids = [row.subj_id for row in rabsence]
    disci = Subject.query.filter(Subject.id.in_(subids))
    values = []
    for row in disci:
        r = {}
        qtaulas = qtAbsence.query.filter_by(subject_id=row.id).count()
        qtdispo = Absence.query.filter_by(subject_id=row.id,user_id=userid).count()

        r['absence'] = qtaulas-qtdispo
        r['presence'] = qtdispo
        r['name'] = f'{row.subname} - {row.subgroup}'

        values.append(r)
    return jsonify({'values': values}), 200


@sapp.route('/createdby/all', methods=['GET'])
@jwt_required
def listsubject():
    userid = get_jwt_identity()
    disci = Subject.query.filter_by(user_id=userid).all()
    values = [row.todict() for row in disci]
    if len(values) == 0:
        return jsonify({'Error':'Nenhuma disciplina cadastrada pelo usuario foi encontrada'}), 404
    data = {}
    data['values'] = values
    return jsonify(data), 200