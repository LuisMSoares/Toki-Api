from flask import Blueprint, request, jsonify
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError #incluir exception dataerror
from app.db import User, Absence, qtAbsence, Subject, Subjectur
from app.db import bluep_db as db

mapp = Blueprint('mapp',__name__)


@mapp.route('/')
def index():
    return 'ola'


def userauth(username,password):
    user = User.query.filter_by(email=username,password=password).first()
    if not user:
        return False
    if user.password == password:
        return user
    return False


@mapp.route('/reguser', methods=['POST'])
def reguser():
    rjson = request.json
    user = User(username=rjson['uname'],
                password=rjson['passw'],
                enrolment=rjson['enrol'],
                email=rjson['email'])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        return jsonify({'Error': 'Já existe um usuario cadastrado com esta matricula ou email!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@mapp.route('/listsubject', methods=['GET'])
def listsubject():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    disci = Subject.query.filter_by(user_id=user.id).all()
    values = [row.todict() for row in disci]
    if len(values) == 0:
        return jsonify({'Error':'Nenhuma disciplina cadastrada pelo usuario foi encontrada'}), 404
    data = {}
    data['values'] = values
    return jsonify(data), 200


@mapp.route('/regsubject', methods=['POST'])
def regsubject():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rjson = request.json
    subject = Subject(user_id=user.id,
                      subname=rjson['sname'],
                      subgroup=rjson['sgroup'])
    try:
        db.session.add(subject)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        return jsonify({'Error': 'Ocorreu algum erro ao tentar realizar o cadastro!'}), 500
    return jsonify({'Success': 'Registro realizado com sucesso'}), 201


@mapp.route('/absence/validade', methods=['POST'])
def abvalidade():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rjson = request.json
    # registro da presença
    absence = Absence(subject_id=rjson['subjid'],
                      user_id=user.id,
                      vdate=rjson['vdate'],
                      device_id=rjson['dvcid'])
    # computação de quantidade de aulas lecionadas
    qtabsence = qtAbsence(subject_id=rjson['subjid'],
                          vdate=rjson['vdate'])
    # relação usuario-disciplina
    subjectur = Subjectur(user_id=user.id,
                          subj_id=rjson['subjid'])
    try:
        try:

            db.session.add(qtabsence)
            db.session.commit()
        except IntegrityError:
            db.session().rollback()
        try:
            db.session.add(subjectur)
            db.session.commit()
        except IntegrityError:
            db.session().rollback()
        db.session.add(absence)
        db.session.commit()
    except IntegrityError as err:
        print(err)
        db.session().rollback()
        absences = Absence.query.filter_by(device_id=rjson['dvcid'],
                                           subject_id=rjson['subjid'],
                                           date=rjson['vdate']).all()
        if absences[0].user_id==user.id:
            return jsonify({'Success': 'Preseça já registrada anteriormente'}), 201
        for row in absences:
            db.session.delete(row)
        db.session.commit()
        return jsonify({'Fraud': 'Dispositivos duplicados detectados, atribuindo falta a ambos os usuarios'}), 201
    return jsonify({'Success': 'Presença computada com sucesso'}), 201


@mapp.route('/subject/relation', methods=['GET'])
def relationsub():
    auth = request.authorization
    user = userauth(auth.username,auth.password)
    if not user:
        return jsonify({'Error':'Ocorreu algum erro ao tentar a autenticação'}), 401
    rabsence = Subjectur.query.filter_by(user_id=user.id)
    if rabsence == None:
        return jsonify({'Error':'Nenhuma disciplina relacionada ao usuario foi encontrada'}), 404
    subids = [row.subj_id for row in rabsence]
    disci = Subject.query.filter(Subject.id.in_(subids))
    values = [row.todict() for row in disci]
    data = {}
    data['values'] = values
    return jsonify(data), 200


@mapp.route('/subject/absence/<int:subjid>', methods=['GET'])
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


@mapp.route('/subject/allabsence/<int:subjid>', methods=['GET'])
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
