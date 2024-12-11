from flask import Flask, request

progress_checker_app = Flask(__name__)
progress_checker_app.secret_key = 'dprada64'

@progress_checker_app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
