from flask import Flask, render_template, request, redirect, url_for, session as flaskSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from custom_exceptions_login import TrackerDNE, UserExists
from sql_tables_python import Users, User_Trackers, Shows

progress_checker_app = Flask(__name__)
progress_checker_app.secret_key = 'dprada64'

@progress_checker_app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
