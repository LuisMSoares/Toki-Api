from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql/projectdb'
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
    return response

if __name__ == '__main__':
    __import__('time').sleep(10)
    app.run(host='0.0.0.0')
