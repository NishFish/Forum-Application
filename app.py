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
        username = request.form['username'].lower()
        password = request.form['password']
        username_store = database_store.users_pass_db.find_one({"username": username})

        if username_store: #check if username is in username_store. If it us, check if the passwords match then proceed
            salt = bcrypt.gensalt()
            check_pass = bcrypt.checkpw(password.encode(), username_store['pass_hash'])
            if check_pass: #if passwords match
                return redirect('/home', code=302)  # go here if password is incorrect
            #must generate an authentication token

        incorrect = "The username or password you entered is Incorrect"
        return render_template('index.html', incorrect=incorrect, mimetype="text/html") #go here if password is incorrect

@app.route('/register', methods=('GET', 'POST')) #register, but not yet complete
def register():
    if request.method == 'POST':
        email = request.form['email'].lower()
        username = request.form['username'].lower()
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if len(email) > 12 and email[-12:] != '@buffalo.edu':
            incorrect = "You must register with an @buffalo.edu email"  # do the same thing with render template if the username already exists
            return render_template('authentication/register.html', incorrect=incorrect, mimetype="text/html")  # go here if password is incorrect

        email_store = database_store.email_db.find_one({"email": email})
        if email_store is not None:
            incorrect = "An account is already registered with this email"  # do the same thing with render template if the username already exists
            return render_template('authentication/register.html', incorrect=incorrect, mimetype="text/html")  # go here if password is incorrect

        username_store = database_store.users_pass_db.find_one({"username": username})
        if username_store is not None:
            incorrect = "This username already exists"  # do the same thing with render template if the username already exists
            return render_template('authentication/register.html', incorrect=incorrect, mimetype="text/html")  # go here if password is incorrect

        if password != password_confirm: #also need to check if email/username are not taken or registered already. Also need to check if email is a buffalo email and send verification email
            incorrect = "Passwords do not match"  # do the same thing with render template if the username already exists
            return render_template('authentication/register.html', incorrect=incorrect, mimetype="text/html")  # go here if password is incorrect

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

@app.route('/home') #reset password
def home():
    return render_template('home/home.html', mimetype="text/html")

@app.route('/template_styling/home.css') #reset password
def home_css():
    return send_file('template_styling/home.css', mimetype="text/css")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
