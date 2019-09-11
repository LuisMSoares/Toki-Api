from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from app.db import SubuserModel, AbsenceModel, AddData, DeleteData


class ValidateAbsenceResource(Resource):
    #json validator: {'subjid':type('string'), 'vdate':type('string'), 'dvcid':type('int')}
    @jwt_required
    def post(self):
        subuser = SubuserModel(sub_id = request.json['subjid'],
                        user_id = get_jwt_identity())
        if not AddData(subuser):
            subuser = SubuserModel.query.filter_by(
                sub_id = request.json['subjid'], user_id = get_jwt_identity()).first()
            subuser.is_active = True
            AddData(subuser)
        absence = AbsenceModel(date = request.json['vdate'],
                        device_id = request.json['dvcid'], 
                        user_absence = subuser,
                        dup_security = request.json['subjid'])
        AddData(absence.PresenceCount(request.json['subjid']))
        if not AddData(absence):
            try:
                absences = AbsenceModel.query.filter_by(device_id = request.json['dvcid'],
                                                dup_security = request.json['subjid'],
                                                date=request.json['vdate']).all()
                if absences[0].user_absence.user_id == get_jwt_identity():
                    return {'success' : 'Preseça já registrada anteriormente'}, 200
                for row in absences:
                    DeleteData(row)
                return {'success' : 'Dispositivos duplicados detectados, atribuindo falta a ambos os usuarios'}, 200
            except IndexError:
                return {'success' : 'Preseça já registrada anteriormente por outro dispositivo'}, 200
        return {'success' : 'Presença computada com sucesso'}, 201