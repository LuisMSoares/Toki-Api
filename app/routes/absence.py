from flask import Blueprint, request, jsonify
from app.db import *
from flask_jwt_extended import ( jwt_required, get_jwt_identity )
from sqlalchemy.orm import load_only

abapp = Blueprint('rabsence',__name__)


@abapp.route('/all/<int:subjid>', methods=['GET'])
@jwt_required
def getallabsences(subjid):    
    ab_users = Subuser.query.filter_by(sub_id=subjid).all()
    if len(ab_users) == 0:
        return jsonify({'Error':'Nenhum discente relacionado a disciplina foi encontrado'}), 404
    presence = Presence.query.filter_by(sub_id=subjid).options(load_only('date'))
    date_presence = [row.date.strftime("%Y-%m-%d") for row in presence]
    qt_presence = len(date_presence)

    values = []
    for ab_user in ab_users:
        v = {}
        absences = ab_user.absences
        qt_absence, user = len(absences), ab_user.user_associate

        v['userid']    = user.id
        v['username']  = f'{user.username} - {user.enrolment}'
        v['presencas'] = qt_absence 
        v['faltas']    = qt_presence - qt_absence

        values.append(v)

    return jsonify({'dates': date_presence, 'values':values}), 200


@abapp.route('/one/subjectId=<int:subjId>&userid=<int:userId>', methods=['GET'])
@jwt_required
def getabsences(subjId, userId):
    subuResult = Subuser.query.filter_by(user_id=userId, sub_id=subjId).first()
    date_presence = [row.date.strftime("%Y-%m-%d") for row in subuResult.absences]
    
    return jsonify({'dates': date_presence}), 200


@abapp.route('/dates/<int:subjId>', methods=['GET'])
@jwt_required
def getPresenceDates(subjId):
    presence = Presence.query.filter_by(sub_id=subjId).options(load_only('date'))
    date_presence = [row.date.strftime("%Y-%m-%d") for row in presence]

    return jsonify({'dates': date_presence}), 200