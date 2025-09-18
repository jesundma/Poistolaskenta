from flask import Flask
from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from service_functions import get_next_project_id, insert_project, get_projects, get_project_by_id
import sqlite3
import db
import config
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0] 
        print(password_hash, username, password, flush=True)

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/main_layout")
        else:
            return "Virhe: Does not Compute"
    
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/main_layout")
def main_layout():
    return render_template("main_layout.html")

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

    return render_template("post_register.html")

@app.route("/post_register_redirect", methods=["POST"])
def post_register_redirect():
    next_page = request.form.get("next", "login")
    if next_page not in ("login", "main_layout"):
        next_page = "login"
    return redirect(url_for(next_page))

@app.route("/new_project", methods=["GET", "POST"])
def new_project():
    if request.method == "POST":
        project_name = request.form["project_name"]
        project_depreciation_method = request.form["project_depreciation_method"]

        project_id = insert_project(project_name, project_depreciation_method)

        return render_template("main_layout.html", message=f"Projekti {project_name} tallennettu tunnuksella {project_id}")
    next_id = get_next_project_id()
    return render_template("new_project.html", next_id=next_id)

@app.route("/list_projects", methods=["GET"])
def list_projects():

    query_projects = get_projects()
    
    projects = []
    
    for row in query_projects:
        project = {
            "project_id": row["project_id"],
            "project_name": row["project_name"],
            "project_depreciation_method": row["project_depreciation_method"]
        }
        projects.append(project)
    
    return render_template("list_projects.html", projects=projects)

@app.route('/cashflow_project')
def cashflow_project():
    project_id = request.args.get('project_id')
    
    investments = get_project_by_id(project_id)

    if investments:
        return render_template('cashflow_project.html', project_id=project_id, investments=investments)
    else:
        return render_template('cashflow_project.html', project_id=project_id, investments=None)