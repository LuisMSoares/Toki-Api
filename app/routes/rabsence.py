from flask import Blueprint, request, jsonify
from app.db import Absence, qtAbsence, Subjectur
from app.db import bluep_db as db
from app.routes import userauth

abapp = Blueprint('rabsence',__name__)


@abapp.route('/subject/absence/<int:subjid>', methods=['GET'])
def getabsences(subjid):
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    qtaulas = qtAbsence.query.filter_by(subject_id=subjid).count()
    qtdispo = Absence.query.filter_by(subject_id=subjid,user_id=user.id).count()
    data = {'subjid':subjid,
            'presencas':qtdispo,
            'faltas':qtaulas-qtdispo }
    return jsonify(data), 200


@abapp.route('/subject/allabsence/<int:subjid>', methods=['GET'])
def getallabsences(subjid):
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401    
    subjectur = Absence.query.distinct(Absence.user_id).filter_by(subject_id=subjid)
    subjectur = Subjectur.query.filter_by(subj_id=subjid)
    if subjectur == None:
        return jsonify({'Error':'Nenhum discente relacionado a disciplina foi encontrado'}), 404
    qtaulas = qtAbsence.query.filter_by(subject_id=subjid).count()
    data = []
    for sur in subjectur:
        dic = {}
        qtdispo = Absence.query.filter_by(subject_id=subjid, user_id=sur.user_id)
        dic[str(sur.user_id)] = [row.date.strftime("%Y-%m-%d") for row in qtdispo]
        dic['presencas'] = qtdispo.count() 
        dic['faltas'] = qtaulas - qtdispo.count()
        data.append(dic)
    return jsonify({'values':data}), 200    
