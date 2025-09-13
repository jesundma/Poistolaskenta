from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import sqlite3
import db
import markupsafe

app = Flask(__name__)

db.init_app(app)

def users_exists():
    try:
        sql = "SELECT COUNT(*) FROM Users"
        con = db.get_connection()
        result = con.execute(sql)
        count = result.fetchone()[0]
        con.close()
        return count > 0
    except sqlite3.OperationalError:
        return None

@app.route("/")
def user_check():
    exists = users_exists()
    if exists is None:
        db.init_db()
        return redirect(url_for("register"))
    elif exists:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("register"))
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"