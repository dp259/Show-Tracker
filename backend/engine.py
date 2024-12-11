from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.custom_exceptions_login import UserNotFound, UserExists, UnauthorizedLogin, UnauthorizedUpdate
from database.sql_tables_python import Users

engine = create_engine("mysql+pymysql://root:root@localhost/progress_checker")

Session = sessionmaker(bind = engine)
session = Session()

def add_user(username, email, password):
    user = session.query(Users).filter((Users.Username == username) | (Users.Email == email)).first()

    if user:
        raise UserExists("Username or email is already in use for another account, pick another.")
    
    new_user = Users(Username = username, Email = email, Password = password)
    session.add(new_user)
    session.commit() 

    print(f"{username} added to database!")
    return True
    
def login_confirmation(username, password):
    user = session.query(Users).filter((Users.Username == username)).first()

    if not user:
        raise UserNotFound("Username not found, try making a account")
    elif user.Password != password:
        raise UnauthorizedLogin("Password is incorrect")
    
    print("Login successful")
    return True

def update_password(user, old, new):
    person = session.query(Users).filter(Users.Username == user).first()

    if not person or person.Password != old:
        raise UnauthorizedUpdate("Incorrect previous username")

    person.Password = new
    session.commit()

def update_username(user, old, new):
    person = session.query(Users).filter(Users.Username == user).first()

    if not person or person.Username != old:
        raise UnauthorizedUpdate("Incorrect previous username")

    person.Username = new
    session.commit()

def update_email(user, old, new):
    person = session.query(Users).filter(Users.Username == user).first()

    if not person or person.Email != old:
        raise UnauthorizedUpdate("Incorrect previous username")

    person.Email = new
    session.commit()