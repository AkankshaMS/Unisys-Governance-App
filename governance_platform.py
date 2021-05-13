import os
import requests
import shutil
import time
from distutils.dir_util import copy_tree
from requests.auth import HTTPBasicAuth
from flask import Flask, redirect, url_for, render_template, request, session, flash
from sqlalchemy import DateTime
#from werkzeug import secure_filename, FileStorage
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.datastructures import  MultiDict
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from flask_restful import Resource, Api
import random
import json
import subprocess
import webbrowser
import patoolib
from pyunpack import Archive
from flask_cors import CORS
from utils import *
import subprocess
from threading import Thread

#to be added as environment variables
# paths["JAVA_HOME"] = 'C:\Program Files\Java\jdk1.8.0_201'
# paths["JBOSS_HOME"] = 'C:/Users/Dell/wildfly-20.0.0.Final'
# paths["WILDFLY_BIN"]='C:/Users/Dell/wildfly-20.0.0.Final/bin/'
# paths["UPLOADS_FOLDER"]='D:/Unisys-Governance-App/uploads'
# paths["WILDFLY_DEPLOYMENTS"]='C:/Users/Dell/wildfly-20.0.0.Final/standalone/deployments/'
paths = load_json_file("paths.json")




#App initialization
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['DEBUG'] = True
socketio = SocketIO(app)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from DataBase import *


current_app_name = None

class AuditApi(Resource):

    def get(self):
        return {'message': 'hello world'}

    def post(self):
        global current_app_name
        print("Post came")
        print()
        data = request.get_json()
        print(data)
        print("BYE")
        operation=data['operation']
        if operation == 'I':
            data['operation'] = 'Insert'
        elif operation == 'U':
            data['operation'] = 'Update'
        elif operation == 'D':
            data['operation'] = 'Delete'
        

        project_name = data['bizDataGroupId']
        print(project_name)
        project = Project.query.filter_by(project_name=project_name).first()
        print(project)
        
        audit = ProjectAudit(auditModuleName=data['auditModuleName'],
            auditDocumentName=data['auditDocumentName'],
            operation=data['operation'],
            userName = data['userName'],
            timestamp = data['timestamp'],proj=project)

        db.session.add(audit)
        db.session.commit()
        if(current_app_name==project_name):
            socketio.emit("audit",data,broadcast=True)
        else:
            print("Not sending")
        #Save the data in database
        #data = {'message': 'hello world'}
        return data
api.add_resource(AuditApi, '/newaudit')





@app.route("/updatepowerstatus",methods=['POST', 'GET'])
def updatepowerstatus():
    print("Came here")
    #print(json.dumps(request.get_data()))
    print(request.get_json())
    print(str(request.get_data()))
    status = request.form['switch_status']
    project = request.form['project']
    print(project,status)

    
    # status=True
    if status == 'false': 
        # os.mkdir(project_name)      
        TurnOn(project)
        
    elif status== 'true':
        TurnOff(project)
        print("Deleted")
    else:
        print("Not found")
    return json.dumps({'msg':'ok'})


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



@app.route("/newapplication", methods=["GET", "POST"])
def newapplication():
    print(request.form)
    print("Hello")
    if request.method == 'POST':
        project_name = request.form['project_name']
        print(project_name)
        database_dialect = request.form['database_dialect']
        print(database_dialect)

        if request.method =='POST':
            file = request.files['file']
        print (file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.chdir(UPLOAD_FOLDER)
        os.getcwd()
        #os.mkdir(filename)
        patoolib.extract_archive(filename, outdir=paths['UPLOADS_FOLDER'])       
        print('File uploaded successfully!')

        
        
        
        project = Project(project_name, database_dialect,
                          file)
        db.session.add(project)
        db.session.commit()



        flash("Project created succesfully")
        #return redirect(request.url)
        return render_template("newApplication.html",Alert="Project created succesfully",Alert_type="success")
    return render_template("newApplication.html")


@app.route("/viewapplications", methods=["GET", "POST"])
def viewapplications():
    project_list = Project.query.all()
    print(project_list)
    return render_template("viewApplications.html", project_list=project_list)
    #values = userDetails.query.all()


@app.route("/applicationinfo/<pname>")
def applicationinfo(pname):
    global current_app_name
    print(pname)
    current_app_name = pname

    project = Project.query.filter_by(project_name=pname).first()
    project_audits = reversed(project.audits) 
    return render_template("applicationinfo.html", project=project,project_audits=project_audits)
    #values = userDetails.query.all()


@app.route("/viewaudit")
def audit():
    project_list = Project.query.all()
    return render_template("viewAudit.html", project_list=project_list)


def start_wildfly_server():
    #for i,project in enumerate(Project.query.all()):
    #    data = {'num':i,'value':'true'}
    #    socketio.emit("switch",data,broadcast=True)
    start_all_projects()

if __name__ == "__main__":
    db.create_all()

    from wildserver import * 
    #start_all_projects()
    wild_thread = Thread(target=start_server,daemon=True)
    wild_thread.start()

    #time.sleep(3)    
    socketio.run(app)
    # app.run(debug=True)
