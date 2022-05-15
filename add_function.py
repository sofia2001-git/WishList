from app.users.user import User
from app.database import db


def add_user(surname, name, age, nick, email, password=None):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.nick = nick
    user.email = email
    if password:
        user.set_password(password)
    db_sess = db.create_session()
    db_sess.add(user)
    db_sess.commit()