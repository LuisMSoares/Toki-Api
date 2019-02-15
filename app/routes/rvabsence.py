from flask import Blueprint, request, jsonify
from app.db import Absence, qtAbsence, Subjectur
from app.db import AddData, DeleteData
from flask_jwt_extended import ( jwt_required, get_jwt_identity )

abvapp = Blueprint('rvabsence',__name__)


@abvapp.route('/validate', methods=['POST'])
@jwt_required
def abvalidade():
    userid = get_jwt_identity()
    rjson = request.json
    # registro da presença
    absence = Absence(subject_id=rjson['subjid'],
                      user_id=userid,
                      vdate=rjson['vdate'],
                      device_id=rjson['dvcid'])
    # computação de quantidade de aulas lecionadas
    qtabsence = qtAbsence(subject_id=rjson['subjid'],
                          vdate=rjson['vdate'])
    # relação usuario-disciplina
    subjectur = Subjectur(user_id=userid,
                          subj_id=rjson['subjid'])
    AddData(qtabsence)
    AddData(subjectur)
    if not AddData(absence):
        absences = Absence.query.filter_by(device_id=rjson['dvcid'],
                                           subject_id=rjson['subjid'],
                                           date=rjson['vdate']).all()
        if absences[0].user_id == userid:
            return jsonify({'success': 'Preseça já registrada anteriormente'}), 200
        for row in absences:
            DeleteData(row)
        return jsonify({'success': 'Dispositivos duplicados detectados, atribuindo falta a ambos os usuarios'}), 200
    return jsonify({'success': 'Presença computada com sucesso'}), 201
