from app.db import User

def userauth(username,password):
    user = User.query.filter_by(email=username,password=password).first()
    if not user:
        return False
    if user.password == password:
        return user
    return False