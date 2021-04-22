import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, redirect, url_for, render_template, request, session, flash
from sqlalchemy import DateTime
#from werkzeug import secure_filename, FileStorage
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from flask_restful import Resource, Api


import random
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['DEBUG'] = True

socketio = SocketIO(app)
api = Api(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))

    #curr_time = db.Column("time", db.DateTime, default = today.strftime("%H:%M:%S"))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Project(db.Model):
    project_id = db.Column("project_id", db.Integer,
                           primary_key=True, autoincrement=True)
    project_name = db.Column("project_name", db.String(100))
    database_dialect = db.Column("database_dialect", db.String(100))
    base_dir = db.Column("base_directory", db.String(100))
    curr_date = db.Column("date", db.DateTime, default=datetime.utcnow)

    def __init__(self, pname, database_dialect, base_dir):
        #self.project_id = random.randint(0,1000)
        self.project_name = pname
        self.database_dialect = database_dialect
        self.base_dir = base_dir


class AuditApi(Resource):

    def get(self):
        return {'message': 'hello world'}

        def post(self):
            print("Post came")
            data = request.get_json()     # status code
            print(data)
            socketio.emit("audit", data, broadcast=True)
            return data


api.add_resource(AuditApi, '/newaudit')


@socketio.on('connect')
def ws_connect():
    print("Connected")


@app.route("/")
def index():
    return redirect("/home")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        '''username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        db.session.add(user)
        db.session.commit()'''
        if request.form['username'] != 'setup' or request.form['password'] != 'setup':
            error = 'Invalid Credentials. Please try again.'
            # print(error)
        else:
            return redirect(url_for('home'))
    return render_template("login.html", error=error)


@app.route("/home")
def home():
    return render_template("home.html")

#app.config["FILE_UPLOADS"] = "/G_Platform/static/img/uploads"


@app.route("/newapplication", methods=["GET", "POST"])
def newapplication():
    print(request.method)
    print("Hello")
    if request.method == 'POST':
        project_name = request.form['project_name']
        print(project_name)
        database_dialect = request.form['database_dialect']
        print(database_dialect)
        print(request.files['file'])

    # check if the post request has the file part
        if 'file' not in request.files:
            print('HI')
            flash('No file part')
            return redirect(request.url)
        project_file = request.files['file']
        # if user does not select file
        if project_file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
        basedir = os.path.abspath(os.path.dirname(__file__))
        project_file.save(os.path.join(
            basedir, "./newapplication", project_file.filename))
        print('File uploaded successfully!')
        project = Project(project_name, database_dialect,
                          project_file.filename)
        db.session.add(project)
        db.session.commit()
        # return basedir
        # return jsonify({"success": True}), 200

    return render_template("newApplication.html")


@app.route("/viewapplications")
def viewapplications():
    project_list = Project.query.all()
    print(project_list)
    return render_template("viewApplications.html", project_list=project_list)
    #values = userDetails.query.all()


@app.route("/applicationinfo/<pname>")
def applicationinfo(pname):
    print(pname)
    project = Project.query.filter_by(project_name=pname).first()
    return render_template("applicationinfo.html", project=project)
    #values = userDetails.query.all()


@app.route("/viewaudit")
def audit():
    project_list = Project.query.all()
    return render_template("viewAudit.html", project_list=project_list)


if __name__ == "__main__":
    db.create_all()
    socketio.run(app)
    # app.run(debug=True)
