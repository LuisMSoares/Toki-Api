from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@postgresql/mydatabase'
db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def index():
    from db.users import Users
    test = Users(username='admin', password='admin', enrolment='admin', email='admin')
    db.session.add(test)
    db.session.commit()
    response = ''
    for i in Users.query.all():
        response += f'{i.id} - {i.username} - {i.enrolment} - {i.email}'
        response += '<br>'
    return response




# reinicie a aplicação apos acessar esta rota
@app.route('/dropall')
def dropall():
    from db import db
    db.drop_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
