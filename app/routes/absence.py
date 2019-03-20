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
    presence = Presence.query.filter_by(sub_id=subjid).options(load_only("date")).all()
    
    date_presence = [ p.date.strftime("%Y-%m-%d") for p in presence ]
    qt_presence = len(presence)

    values = []
    for ab_user in ab_users:
        v = {}
        absences = ab_user.absences
        qt_absence, user = len(absences), ab_user.user_associate

        v['userid']    = user.id
        v['username']  = f'{user.username} - {user.enrolment}'
        v['presencas'] = qt_absence 
        v['faltas']    = qt_presence - qt_absence
        v['dates']     = [row.date.strftime("%Y-%m-%d") for row in absences]

        values.append(v)

    return jsonify({'ldates':date_presence, 'values':values}), 200  


@abapp.route('/one/<int:subjid>', methods=['GET'])
@jwt_required
def getabsences(subjid):
    subuser = Subuser.query.filter_by(user_id=get_jwt_identity(),
                                      sub_id=subjid).first()
    dates = [absc.date.strftime("%Y-%m-%d") for absc in subuser.absences]
    return jsonify({'dates':dates}), 200

