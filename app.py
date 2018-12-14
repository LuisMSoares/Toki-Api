from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgresql/projectdb'
db = SQLAlchemy(app)


def dbcommit(obj):
    db.session.add(obj)
    db.session.commit()

@app.route('/')
def index():
    from db.tables import User, Subject, Absence
    dbcommit(User(username='Luis Eduardo', 
        password='1234', enrolment='2749', email='dudu@dudu'))
    dbcommit( Subject(user_id=1, subname='Teste Disciplina', subgroup=1337) )
    dbcommit( Absence(subject_id=1, user_id=1, sdate='2018-12-14') )
    return 'Commit data'


def recreate_db():
    from db import db
    db.drop_all()
    db.create_all()
    print(' * Recreating Database')
if __name__ == '__main__':
    recreate_db() # comment this line to deactivate
    app.run(host='0.0.0.0',debug=True)
