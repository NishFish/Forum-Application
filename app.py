from flask import Flask, render_template, send_file, request, url_for, redirect, abort, make_response
from pymongo import MongoClient
from secure import Secure
secure_headers = Secure()
import bcrypt
import random
import string
import hashlib
import database_store
import sys

app = Flask(__name__)

#Security Considerations
#x-content-type nosniff set by secure on all responses
#html escaped in all form data that can be requested by some user
#all passwords stored hashed and salted
#auth tokens stored hashed
#auth tokens cookie set http only
#all private pages redirect to login if user is not authenticated


def escapeHTML(input):
    return input.replace('&', "&amp;").replace('<', "&lt").replace('>', "&gt")

@app.route('/') #page that shows when website first loags and user is not logged in
def default_page():
    return render_template('index.html', mimetype="text/html")

@app.route('/template_styling/login.css') #CSS file for login
def login_css():
    return send_file('template_styling/login.css', mimetype="text/css")

@app.route('/images/temporary.png') #temporary image
def temporary_image():
    return send_file('images/temporary.png')

@app.route('/images/logo.png') #UB logo
def logo():
    return send_file('images/logo.png')

@app.route('/login', methods=('GET', 'POST')) #login, but not yet complete
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username_store = database_store.users_pass_db.find_one({"username": username})
        #check if username is in username_store. If it us, check if the passwords match then proceed 
        if username_store:
            salt = bcrypt.gensalt()
            pass_hash = bcrypt.hashpw(password.encode(), salt)
            check_pass = bcrypt.checkpw(password.encode(), username_store['pass_hash'])
            print(check_pass, flush=True)
            #must generate an authentication token

    return render_template('index.html', mimetype="text/html")

@app.route('/register', methods=('GET', 'POST')) #register, but not yet complete
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']


        if password == password_confirm: #also need to check if email/username are not taken or registered already. Also need to check if email is a buffalo email and send verification email
            salt = bcrypt.gensalt()
            pass_hash = bcrypt.hashpw(password.encode(), salt)
            database_store.users_pass_db.insert_one({'username': username, 'pass_hash': pass_hash}) #insert into database
            database_store.email_db.insert_one({'username': username, 'email': email})# insert into database
            return render_template('authentication/successfull_register.html', mimetype="text/html"), {"Refresh": "3; url=/"} #redirects to main page




@app.route('/template_styling/register.css') #register css
def register_css():
    return send_file('template_styling/register.css', mimetype="text/css")

@app.route('/register_page') #main register page
def register_page():
    return render_template('authentication/register.html', mimetype="text/html")

@app.route('/reset') #reset password
def reset():
    return render_template('authentication/reset_password.html', mimetype="text/html")




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
