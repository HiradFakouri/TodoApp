from flask import Flask, render_template, request, redirect, flash, session
import pymongo
import os
from dotenv import load_dotenv

###########  Encryption ###########
"""
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
"""

#encryption - have to work on it later
#salt = os.getenv('salt')
#password = os.getenv('password')

#key = PBKDF2(password, salt, dkLen=32)

#cipher = AES.new(key, AES.MODE_CBC)
#hashedPassword = cipher.encrypt(pad(password.encode("utf-8"), AES.block_size))
#decryptedPassword = unpad(cipher.decrypt(datapassword), AES.block_size)

###########  Encryption ###########

#loading the mongodb_url
load_dotenv()
mongo_url = os.getenv('mongo_url')

#connecting to database
cluster = pymongo.MongoClient(mongo_url)
db = cluster["TodoApp"]
collection = db["Users"]

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            pass
        else:
            return render_template('todo.html', user=username)
    else:
        return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "" or password == "":
            flash("field is empty", category="error")
            return redirect(request.url)
        
        if collection.find_one({"username": username}) == None:
            flash("username doesn't exsits", category="error")
            return redirect(request.url)
        
        data = collection.find_one({"username": username})
        datapassword = data["password"]

        if password != datapassword:
            flash("The password is incorrect", category="error")
            return redirect(request.url)

        session["username"] = username

        return redirect("/todo")
        
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        conPassword = request.form.get('confirmPassword')

        if username == "" or password == "" or conPassword == "":
            flash("field is empty", category="error")
            return redirect(request.url)

        if not password == conPassword:
            flash("passwords do not match", category="error")
            return redirect(request.url)

        if not collection.find_one({"username": username}) == None:
            flash("username already exsits", category="error")
            return redirect(request.url)

        collection.insert_one({"username": username, "password": password, "todo": []})

        return redirect("/login")
    else:
        return render_template('signup.html', error="")