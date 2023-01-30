from flask import Flask, render_template, request, redirect
import pymongo
import os
from dotenv import load_dotenv
import hashlib

#loading the mongodb_url
load_dotenv()
mongo_url = os.getenv('mongo_url')

#connecting to database
cluster = pymongo.MongoClient(mongo_url)
db = cluster["TodoApp"]
collection = db["Users"]

#collection.insert_one({"username": "Hirad", "password": "1234"})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        conPassword = request.form.get('confirmPassword')

        if password != conPassword:
            error = "passwords do not match"
            return redirect('/signup')

        if collection.find({"username": username}) == None:
            error = "username is taken"
            return redirect('/signup')

        #not working properly
        hashedPassword = hashlib.sha256(password.encode('utf8'))
        collection.insert_one({"username": username, "password": hashedPassword.digest(), "todo": []})

        return redirect("/login")
    else:
        return render_template('signup.html', error="")