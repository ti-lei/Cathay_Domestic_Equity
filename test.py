# This Python file uses the following encoding: utf-8
# encoding: utf-8
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import requests
import json
import datetime
import pandas as pd
import os
import shutil
import datetime

app = Flask(__name__, static_folder='static', static_url_path='')

username = 'cathayequity'
password = '123'
# datetime.datetime.now().strftime("%Y%m%d")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('123')
    if request.method == 'POST':
        # Get Form Fields
        username_candidate = request.form.get('username',False)
        password_candidate = request.form.get('password',False)
        print(username_candidate)
        print(password_candidate)

        if username_candidate == username:

            if password == password_candidate:
                # Passed
                session['logged_in'] = True
                session['username'] = username

                # flash('You are now logged in', 'success')
                return redirect(url_for('abc'))
            else:
                error = 'Wrong Password'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route("/home")
@is_logged_in
def abc():
	return 'ok'

@app.route("/")
def start():
	return redirect(url_for('login'))

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.secret_key = 'secret123'
    app.run(debug=True)
