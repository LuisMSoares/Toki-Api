from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from sqlalchemy.orm import load_only
from datetime import datetime
from app.db import SubuserModel, PresenceModel, AddData


class AbsenceResource(Resource):
    @jwt_required
    def get(self):
        if request.args.get('presence', '0') == '1':
            return self.getPresenceDates(int(request.args.get('subjid', 0)))
        if request.args.get('all', '0') == '1':
            return self.getallabsences(int(request.args.get('subjid', 0)))
        if request.args.get('one', '0') == '1':
            return self.getabsences(int(request.args.get('subjid', 0)), int(request.args.get('userId', 0)))
        return {'message': 'Codigo da disciplina e/ou do usuário não encontrado!'}, 404

    def getPresenceDates(self, subjId):
        presence = PresenceModel.query.filter_by(sub_id=subjId).options(load_only('date'))
        date_presence = [row.date.strftime("%Y-%m-%d") for row in presence]
        return {'dates': date_presence}, 200
        
    def getallabsences(self, subjid):
        ab_users = SubuserModel.query.filter_by(sub_id=subjid).all()
        if len(ab_users) == 0:
            return {'Error':'Nenhum discente relacionado a disciplina foi encontrado'}, 404
        ab_users.sort(key=lambda x: int(x.user_associate.enrolment))
        presence = PresenceModel.query.filter_by(sub_id=subjid).options(load_only('date'))
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
        return {'dates': date_presence, 'values':values}, 200

    def getabsences(self, subjId, userId):
        subuResult = SubuserModel.query.filter_by(user_id=userId, sub_id=subjId).first()
        absences = subuResult.absences
        if absences:
            date_presence = [row.date.strftime("%Y-%m-%d") for row in absences]
            current_date = absences[-1].date.strftime("%Y-%m-%d")
        else:
            date_presence = []
            current_date = datetime.now().strftime("%Y-%m-%d")
        return {'current': current_date, 'dates': date_presence}, 200
