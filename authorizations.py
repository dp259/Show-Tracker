from flask import Blueprint, render_template, request, redirect, url_for, flash, session as flaskSession
from engine import add_user, login_confirmation, update_email, update_password, update_username
from custom_exceptions_login import UserExists, UnauthorizedLogin, UserNotFound, UnauthorizedUpdate

authorization_bp = Blueprint('authorization_bp', __name__)

@authorization_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']

        try:
            if add_user(username, email, password):
                flash(f'Successfully Registered {username}!')
                return redirect(url_for("authorization_bp.login"))
            else:
                flash("Registration failed, please try again.")
        except UserExists:
            flash("Username or email already exists, try another one.")
    return render_template("user/registration.html")

@authorization_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        try:
            if login_confirmation(username, password):
                flaskSession['Username'] = username
                flash(f'{username} successfully logged in!')
                return redirect(url_for("tracker_bp.tracker_ui"))
            else:
                flash("Login attempt failed, please try again.")
        except UserNotFound:
            flash(f'{username} does not exist.')
        except UnauthorizedLogin:
            flash('Password is incorrect please try again.')
    return render_template("user/login_page.html")

@authorization_bp.route('/settings', methods = ['GET', 'POST'])
def settings():
    if 'Username' not in flaskSession:
        return redirect(url_for('authorization_bp.login'))
    
    if request.method == 'POST':
        try:
            username = flaskSession['Username']
            button = request.form.get('btn')

            if button == 'change_username':
                oldUsername = request.form['old_username']
                newUsername = request.form['new_username']
                update_username(username, oldUsername, newUsername)
                flash(f"Username successfully changed to {newUsername}")
            if button == 'change_email':
                oldEmail = request.form['old_email']
                newEmail = request.form['new_email']
                update_email(username, oldEmail, newEmail)
                flash(f"Email successfully changed to {newEmail}")
            if button == 'change_password':
                oldPass = request.form['old_password']
                newPass = request.form['new_password']
                update_password(username, oldPass, newPass)
                flash("Password successfully updated!")
        except UnauthorizedUpdate:
            flash("Old email, password or username must reflect the current one you are logged into.")
            return redirect(url_for('authorization_bp.start_setting'))
    return redirect(url_for('authorization_bp.start_setting'))

@authorization_bp.route('/start_setting')
def start_setting():
    if 'Username' not in flaskSession:
        return redirect(url_for('authorization_bp.login'))
    return render_template("user/settings.html")

@authorization_bp.route('/logout')
def logout():
    flaskSession.pop('Username', None)
    flash('You have been logged out.')
    return redirect(url_for("authorization_bp.login"))