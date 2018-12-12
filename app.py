from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql/projectdb'
db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def index():
    return 'nada'


if __name__ == '__main__':
    from db.users import Users
    test = Users(username='admin', password='admin', enrolment='admin', email='admin')
    db.session.add(test)
    db.session.commit()

    print('\n\n\n\n')
    for i in Users.query.all():
        print(f'{i.id} - {i.username} - {i.enrolment} - {i.email}')
    print('\n\n\n\n')

    app.run(host='0.0.0.0')
