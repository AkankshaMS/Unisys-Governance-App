import os
import requests
import shutil
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
#to be added as environment variables
os.environ["JAVA_HOME"] = 'C:\Program Files\Java\jdk1.8.0_201'
os.environ["JBOSS_HOME"] = 'C:/Users/Dell/wildfly-20.0.0.Final'
os.environ["WILDFLY_BIN"]='C:/Users/Dell/wildfly-20.0.0.Final/bin/'
os.environ["UPLOADS_FOLDER"]='D:/Unisys-Governance-App/uploads'
os.environ["WILDFLY_DEPLOYMENTS"]='C:/Users/Dell/wildfly-20.0.0.Final/standalone/deployments/'

def navigate_and_renamejson(src,project_name):
    new_json=project_name+'.json'
    
    for item in os.listdir(src):
        s = os.path.join(src, item)      
        if s.endswith(".json"):
            shutil.copy(s, os.path.join(src, new_json))
    with open(new_json, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('ecommerce', project_name)
    with open(new_json, 'w') as file:
        file.write(filedata)
 
              

def navigate_and_renameds(src,project_name):
    new_ds=project_name+'-ds.xml'
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if s.endswith("-ds.xml"):
            shutil.copy(s, os.path.join(src, new_ds))
    with open(new_ds, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('ecommerce', project_name)
    with open(new_ds, 'w') as file:
        file.write(filedata)
 

def TurnOn(project_name):
    dir_src = os.environ['WILDFLY_DEPLOYMENTS']
    os.getcwd()
    os.chdir(os.environ['WILDFLY_BIN'])
    os.getcwd()
    print ("Wildfly started successfully")
    url = 'http://localhost:8080/'+project_name
    webbrowser.register('chrome', 
    None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(url)
    os.system('standalone.bat')

def TurnOff(project_name):
    os.getcwd()
    os.chdir(os.environ['WILDFLY_BIN'])
    os.getcwd()
    os.system('jboss-cli.bat --connect command=:reload')
    print ("wildfly restarted successfully")

    

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
    project_name=project+'.war'
    project_json=project+'.json'
    project_ds=project+'-ds.xml'
    src_path=os.environ['UPLOADS_FOLDER']+"/"+project_name
    src_json=os.environ['UPLOADS_FOLDER']+"/"+project_json
    src_ds=os.environ['UPLOADS_FOLDER']+"/"+project_ds
    d_path=os.environ['WILDFLY_DEPLOYMENTS']
    # del_path="C:/Users/Dell/wildfly-20.0.0.Final/standalone/deployments/"+project_name
    del_path=os.environ['WILDFLY_DEPLOYMENTS']+project_name
    del_json=d_path+project_json
    del_ds=d_path+project_ds
    # status=True
    if status == 'false': 
        # os.mkdir(project_name)      
        copy_tree(src_path, d_path+project_name)
        shutil.copy(src_json,d_path)
        shutil.copy(src_ds,d_path)
        print("Copied")
        TurnOn(project)
        
    elif status== 'true':
        shutil.rmtree(del_path,ignore_errors=True)
        os.remove(del_ds)
        os.remove(del_json)
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
        # files = request.files.getlist('files[]')
        # print(files)
        # for file in files:
        #     # if file (file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if request.method =='POST':
            file = request.files['file']
        print (file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.chdir(UPLOAD_FOLDER)
        os.getcwd()
        #os.mkdir(filename)
        patoolib.extract_archive(filename, outdir=os.environ['UPLOADS_FOLDER'])       
        print('File uploaded successfully!')
        d_path=os.environ['UPLOADS_FOLDER']
        navigate_and_renamejson(d_path,project_name)
        print("JSON file created")
        navigate_and_renameds(d_path,project_name)
        print("DS file created")



        # print("File is",request.files['file'])
        # # check if the post request has the file part
        # if 'file' not in request.files:
        #     print('HI')
        #     flash('No file part')
        #     return redirect(request.url)
        # project_file = request.files['file']
        # # if user does not select file
        # if project_file.filename == '':
        #     flash('No selected file')
        #     # return redirect(request.url)
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # project_file.save(os.path.join(
        #     basedir, "./newapplication", project_file.filename))
        # print('File uploaded successfully!')
        
        
        
        
        
        
        project = Project(project_name, database_dialect,
                          file)
        db.session.add(project)
        db.session.commit()




        
        #Aka
        # return basedir
        # return jsonify({"success": True}), 200
        flash("Project created succesfully")
        return redirect(request.url)
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


if __name__ == "__main__":
    db.create_all()
    socketio.run(app)
    # app.run(debug=True)
