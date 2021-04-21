from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

#configure db
db = yaml.load(db.yaml)
app.configure['MYSQL_HOST'] = db['mysql_host']
app.configure['MYSQL_USER'] = db['mysql_user']
app.configure['MYSQL_PASSOWORD'] = db['mysql_password']
app.configure['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/newapplication", methods = ['GET', 'POST'])
def newapplication():
	if request.method == 'POST':
		#fetch the form data
		userDetails = request.form
		projectName = userDetails['projectName']
		databaseDialect = userDetails['databaseDialect']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO userDetails(projectName, databaseDialect) VALUES(%s, %s)", (projectName, databaseDialect))
		mysql.connection.commit()
		cur.close()
		return 'success'
	return render_template("newApplication.html")

@app.route("/viewapplication")	
def viewapplication():

	return render_template("viewApplication.html")

@app.route("/audit")
def audit():

	return render_template("audit.html")

if __name__== "__main__":
	app.run(debug=True)

