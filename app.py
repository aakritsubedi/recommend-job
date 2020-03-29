import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('layout.html')


