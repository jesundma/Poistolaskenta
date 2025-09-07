from flask import Flask
from flask import render_template
import markupsafe

app = Flask(__name__)

@app.route('/')
def home():
    return "In the beginning, there was nothing."

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/database_management')
def database_management():
    return render_template('database_management.html')
