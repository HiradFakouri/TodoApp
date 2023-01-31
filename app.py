from flask import Flask, render_template, request, redirect, flash
import pymongo
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

#loading the mongodb_url
load_dotenv()
mongo_url = os.getenv('mongo_url')

#config fernet
key = Fernet.generate_key()
fernet = Fernet(key)

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

@app.route('/todo')
def todo():
    return render_template('todo.html')

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

        #decryption not working
        decryptedPassword = fernet.decrypt(datapassword).decode()

        if password != decryptedPassword:
            flash("The password is incorrect", category="error")
            return redirect(request.url)

        return redirect("/todo")
        
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global fernet

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
        
        hashedPassword = fernet.encrypt(password.encode())
        collection.insert_one({"username": username, "password": hashedPassword, "todo": []})

        return redirect("/login")
    else:
        return render_template('signup.html', error="")