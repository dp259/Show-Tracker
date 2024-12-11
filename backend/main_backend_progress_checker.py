from flask import Flask
from backend.authorizations import authorization_bp
from backend.tracker_routes import tracker_bp

#Creating app and engine and session to actually access database and begin the flask setup
progress_checker_app = Flask(__name__)
progress_checker_app.secret_key = 'dprada06-05-2002_Duke_University_Rules_Type_Shiiii!!'

progress_checker_app.register_blueprint(authorization_bp)
progress_checker_app.register_blueprint(tracker_bp)
""""
with Session() as session:
    result = session.execute(text("SELECT * FROM Shows LIMIT 5"))
    for row in result:
        print(row)
"""

"""
=============================================================================================================================================================
Functions to add a new user with proper exceptions in place and another to actually attempt to login with proper exceptions in place to prevent fault logins.
=============================================================================================================================================================
"""       
if __name__ == '__main__':
    progress_checker_app.run(debug=True)
#Checking to make sure error cases work
"""
create = input("Create a new user? (y/n)")

if create == 'y':
    success = False
    while not success:
        username = input("Type in your username: ")
        email = input("Type in your email: ")
        password = input("Type in your password: ")
        success = add_user(username, email, password)
else:
    success = False
    while not success:
        username_email = input("Type in your username? ")
        password = input("What is your password? ")
        success = login_confirmation(username_email, password)
"""