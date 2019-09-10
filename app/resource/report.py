from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.orm import load_only
from app.db import SubuserModel, PresenceModel
from app.services import Excel


class ReportResource(Resource):
    @jwt_required
    def get(self, subjid):
        ab_users = SubuserModel.query.filter_by(sub_id=subjid).all()
        if len(ab_users) == 0:
            return {'Error':'Nenhum discente relacionado a disciplina foi encontrado'}, 404
        ab_users.sort(key=lambda x: int(x.enrolment))
        presence = PresenceModel.query.filter_by(sub_id=subjid).options(load_only('date'))
        qt_presence = len(presence)
        values = []
        for ab_user in ab_users:
            v = {}
            absences = ab_user.absences
            qt_absence, user = len(absences, ab_user.user_associate)
            v['nome']  = user.username
            v['matricula'] = user.enrolment
            v['faltas']    = qt_presence - qt_absence
            v['presencas'] = qt_absence
            values.append(v)
        return Excel.report_from_records(values, 'xlx', 'Relatorio de Faltas')