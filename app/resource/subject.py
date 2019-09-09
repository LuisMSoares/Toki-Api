from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from app.db import UserModel, SubjectModel, SubuserModel, AddData, DeleteData


class OwnerSubjectResource(Resource):
    @jwt_required
    def get(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        values = []
        for subj in user.my_subject:
            v = {}
            v['id'] = subj.id
            v['subgroup'] = subj.sub_group
            v['subname'] = subj.sub_name
            v['user_id'] = subj.user_id
            values.append(v)
        return {'values': values}, 200

    #json validator: {'sname':type('string'), 'sgroup':type('string')}
    @jwt_required
    def post(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        subject = SubjectModel(sub_name=request.json['sname'],
                        sub_group=request.json['sgroup'],
                        creator=user)
        if not AddData(subject):
            return {'Error': 'Preencha todos os campos corretamente!'}, 500
        return {'Success': 'Registro realizado com sucesso'}, 201

    #json validator: {'sname':type('string'), 'sgroup':type('string'), 'sid':type('int'), 'upass':type('string')}
    @jwt_required
    def put(self, subject_id=None):
        if subject_id:
            return self.deleteSubject(subject_id)

        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user.verify_password(request.json['upass']):
            return {'Error': 'Senha informada incorreta!'}, 401
        subject = SubjectModel.query.filter_by(id=request.json['sid']).first()
        if subject == None:
            return {'Error': 'Registro não encontrado'}, 404
        subject.sub_name = request.json['sname']
        subject.sub_group = request.json['sgroup']
        if not AddData(subject):
            return {'Error': 'Preencha todos os campos corretamente!'}, 500
        return {'Success': 'Registro realizado com sucesso'}, 200
    
    #json validator: {'upass':type('string'),}
    def deleteSubject(self, subject_id):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user.verify_password(request.json['upass']):
            return {'Error': 'Senha informada incorreta!'}, 401
        subj = SubjectModel.query.filter_by(id=subject_id).first()
        if not DeleteData(subj):
            return {'Error': 'Ocorreu algum erro ao deletar a disciplina'}, 400
        return {'Success': 'Disciplina removida com sucesso'}, 200


class AssociateSubjectResource(Resource):
    @jwt_required
    def get(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        values, my_associations = [], user.subj_associated
        if len(my_associations) == 0:
            return {'Error':'Nenhuma disciplina relacionada ao usuario foi encontrada'}, 404
        for sjuser in my_associations:
            if sjuser.is_active:
                v, qtpresence = {}, len(sjuser.subj_associate.presence_count)
                qtabsence = len(sjuser.absences)
                # user data
                v['suid'] = sjuser.id
                v['userid'] = user.id
                v['absence'] = qtpresence - qtabsence
                v['presence'] = qtabsence
                # subject data
                v['subid'] = sjuser.subj_associate.id
                v['subname'] = sjuser.subj_associate.sub_name
                v['subgroup'] = sjuser.subj_associate.sub_group
                values.append(v)
        return {'values': values}, 200


    @jwt_required
    #json validator: {'suid':type('int'),}
    def put(self):
        try:
            subuser = SubuserModel.query.filter_by(
                id=request.json['suid'], user_id=get_jwt_identity()).first()
            subuser.is_active = False
            AddData(subuser)
        except:
            pass
        return {'Success': 'Disciplina desativada com sucesso'}, 200
