from flask import Flask, render_template, send_file, request, url_for, redirect, abort, make_response
from pymongo import MongoClient
from secure import Secure
secure_headers = Secure()
import bcrypt
import random
import string
import hashlib
import database_store

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

@app.route('/login') #login, but not yet complete
def login():
    return render_template('index.html', mimetype="text/html")

@app.route('/register') #register, but not yet complete
def register():
    print(request)
    return render_template('index.html', mimetype="text/html")

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
