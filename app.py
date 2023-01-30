from flask import Flask, render_template
import pymongo
import os
from dotenv import load_dotenv

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
    return render_template('signup.html')