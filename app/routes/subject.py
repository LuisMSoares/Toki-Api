from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from app.db import *
from flask_jwt_extended import ( jwt_required, get_jwt_identity )
from app.routes import json_verification

sapp = Blueprint('rsubject',__name__)


@sapp.route('/register', methods=['POST'])
@jwt_required
def regsubject():
    keys, rjson = ['sname','sgroup'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    user = User.query.filter_by(id=get_jwt_identity()).first()
    subject = Subject(sub_name=rjson['sname'],
                      sub_group=rjson['sgroup'],
                      creator=user
    )
    if not AddData(subject):
        return jsonify({'Error': 'Preencha todos os campos corretamente!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


# trocar para PUT no react native e aqui
@sapp.route('/edit', methods=['POST'])
@jwt_required
def editsubject():
    keys, rjson = ['sname','sgroup','sid'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    subject = Subject.query.filter_by(id=rjson['sid']).first()
    if subject == None:
        return jsonify({'Success': 'Registro não encontrado'}), 404
    
    subject.sub_name  = rjson['sname']
    subject.sub_group = rjson['sgroup']

    if not AddData(subject):
        return jsonify({'Error': 'Preencha todos os campos corretamente!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@sapp.route('/delete', methods=['DELETE'])
@jwt_required
def deletesubject():
    keys, rjson = ['sid'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    subj = Subject.query.filter_by(id=rjson['sid']).first()

    if not DeleteData(subj):
        return jsonify({'Error': 'Ocorreu algum erro ao deletar a disciplina'}), 400
    return jsonify({'Success': 'Disciplina removida com sucesso'}), 200


@sapp.route('/association/disable', methods=['PUT'])
@jwt_required
def subjdisable():
    keys, rjson = ['suid'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400
    try:
        subuser = Subuser.query.filter_by(
            id=rjson['suid'], user_id=get_jwt_identity()).first()
        subuser.is_active = False
        AddData(subuser)
    except:
        pass

    return jsonify({'Success': 'Disciplina desativada com sucesso'}), 200


@sapp.route('/enrolled/all', methods=['GET'])
@jwt_required
def relationsub():
    user = User.query.filter_by(id=get_jwt_identity()).first()

    values, my_associations = [], user.subj_associated
    if len(my_associations) == 0:
        return jsonify({'Error':'Nenhuma disciplina relacionada ao usuario foi encontrada'}), 404

    for sjuser in my_associations:
        if sjuser.is_active:
            v, qtpresence = {}, len(sjuser.subj_associate.presence_count)
            qtabsence = len(sjuser.absences)

            v['suid']     = sjuser.id
            v['absence']  = qtpresence - qtabsence
            v['presence'] = qtabsence
            v['name']     = sjuser.subj_associate.sub_name

            values.append(v)

    return jsonify({'values': values}), 200


@sapp.route('/createdby/all', methods=['GET'])
@jwt_required
def listsubject():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    
    values = []
    for subj in user.my_subject:
        v = {}
        v['id']       = subj.id
        v['subgroup'] = subj.sub_group
        v['subname']  = subj.sub_name
        v['user_id']  = subj.user_id

        values.append(v)
    
    return jsonify({'values': values}), 200