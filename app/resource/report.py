from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.orm import load_only
from app.db import SubuserModel, PresenceModel
from app.services import Excel


class ReportResource(Resource):
    @jwt_required
    def get(self, subject_id):
        
        ab_users = SubuserModel.query.filter_by(sub_id=subject_id).all()
        if len(ab_users) == 0:
            return {'Error':'Nenhum discente relacionado a disciplina foi encontrado'}, 404
        ab_users.sort(key=lambda x: int(x.user_associate.enrolment))
        contains = lambda x,y: ['V' if i in y else 'X' for i in x]

        presence = PresenceModel.query.filter_by(sub_id=subject_id).options(load_only('date'))
        subject_presence_count = [row.date.strftime("%Y-%m-%d") for row in presence]
        qt_presence = len(subject_presence_count)
        values = [['Nome', 'Identificação', 'Quantidade de Faltas', 'Quandidade de Presencas']+subject_presence_count]
        
        for ab_user in ab_users:
            user_presences = [row.date.strftime("%Y-%m-%d") for row in ab_user.absences]
            qt_absence, user = len(user_presences), ab_user.user_associate

            values.append([
                user.username, #Nome
                user.enrolment, #Identificação
                qt_presence - qt_absence, #Total de Faltas
                qt_absence, #Total de Presenças
            ]+contains(subject_presence_count, user_presences))
        #return values, 200
        return Excel.report_by_array(values, 'xls', 'Relatorio de Faltas')