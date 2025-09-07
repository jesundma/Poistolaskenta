from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import db
import markupsafe

app = Flask(__name__)

def users_exists():
    sql = "SELECT COUNT(*) FROM Users"
    con = get_connection()
    result = con.execute(sql)
    count = result.fetchone()[0]
    con.close()
    return count > 0


@app.route("/")
def user_check():
    if users_exist():
        return redirect(url_for("login"))
    else:
        return redirect(url_for("register"))
    
@app.route('/index')
def index():
    return render_template('index.html')

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