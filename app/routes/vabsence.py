from flask import Blueprint, request, jsonify
from app.db import *
from flask_jwt_extended import ( jwt_required, get_jwt_identity )
from app.routes import json_verification

abvapp = Blueprint('rvabsence',__name__)


@abvapp.route('/validate', methods=['POST'])
@jwt_required
def abvalidade():
    keys, rjson = ['subjid','vdate','dvcid'], request.json
    if not json_verification(json_data=rjson, keys=keys):
        return jsonify({'Error': 'Invalid json request data'}), 400

    subuser  = Subuser(sub_id = rjson['subjid'],
                       user_id = get_jwt_identity()
    )
    if not AddData(subuser):
        subuser = Subuser.query.filter_by(
            sub_id=rjson['subjid'], user_id=get_jwt_identity()).first()
        subuser.is_active = True
        AddData(subuser)

    absence  = Absence(date = rjson['vdate'],
                       device_id = rjson['dvcid'], 
                       user_absence = subuser,
                       dup_security = rjson['subjid']
    )
    AddData( absence.PresenceCount( rjson['subjid'] ) )

    if not AddData(absence):
        try:
            absences = Absence.query.filter_by(device_id=rjson['dvcid'],
                                            dup_security = rjson['subjid'],
                                            date=rjson['vdate']).all()
            if absences[0].user_absence.user_id == get_jwt_identity():
                return jsonify({'success': 'Preseça já registrada anteriormente'}), 200
            for row in absences:
                DeleteData(row)
            return jsonify({'success': 'Dispositivos duplicados detectados, atribuindo falta a ambos os usuarios'}), 200
        except IndexError:
            return jsonify({'success': 'Preseça já registrada anteriormente por outro dispositivo'}), 200
    return jsonify({'success': 'Presença computada com sucesso'}), 201
