from app.db import bluep_db as db
from app.db import User

class Subject(db.Model):
    __tablename__ = 'disciplina'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    subname = db.Column(db.String(80), nullable=False)
    subgroup = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, subname, subgroup):
        self.user_id = user_id
        self.subname = subname
        self.subgroup = subgroup
    
    def todict(self):
        keys = ['id', 'user_id', 'subname', 'subgroup']
        values = [self.id, self.user_id, self.subname, self.subgroup]
        return dict(zip(keys,values))
