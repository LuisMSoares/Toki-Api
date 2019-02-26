from flask import Blueprint, request, jsonify
from app.db import *
from flask_jwt_extended import ( jwt_required, get_jwt_identity )

abapp = Blueprint('rabsence',__name__)


@abapp.route('/all/<int:subjid>', methods=['GET'])
@jwt_required
def getallabsences(subjid):    
    ab_users = Subuser.query.filter_by(sub_id=subjid).all()
    if len(ab_users) == 0:
        return jsonify({'Error':'Nenhum discente relacionado a disciplina foi encontrado'}), 404
    qt_presence = Presence.query.filter_by(sub_id=subjid).count()

    values = []
    for ab_user in ab_users:
        v = {}
        qt_absence, user = len(ab_user.absences), ab_user.user_associate

        v['username']  = f'{user.username} - {user.enrolment}'
        v['presencas'] = qt_absence 
        v['faltas']    = qt_presence - qt_absence
        #v['dates']     = [row.date.strftime("%Y-%m-%d") for row in qtdispo]

        values.append(v)

    return jsonify({'values':values}), 200  


#-not-used-----------------------------------------------------------------------
@abapp.route('/one/<int:subjid>', methods=['GET'])
@jwt_required
def getabsences(subjid):
    user = User.query.filter_by(id=get_jwt_identity()).first()

    userid = get_jwt_identity()
    qtaulas = qtAbsence.query.filter_by(subject_id=subjid).count()
    qtdispo = Absence.query.filter_by(subject_id=subjid,user_id=userid).count()
    data = {'subjid':subjid,
            'presencas':qtdispo,
            'faltas':qtaulas-qtdispo }
    return jsonify(data), 200

