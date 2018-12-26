from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db import Absence, qtAbsence, Subjectur
from app.db import bluep_db as db
from app.routes import userauth

abvapp = Blueprint('rvabsence',__name__)


@abvapp.route('/absence/validade', methods=['POST'])
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
