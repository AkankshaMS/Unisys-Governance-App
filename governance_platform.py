from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/home")
def home():

	return render_template("home.html")

@app.route("/newapplication")
def newapplication():

	return render_template("newApplication.html")

@app.route("/viewapplication")	
def viewapplication():

	return render_template("viewApplication.html")

@app.route("/audit")
def audit():

	return render_template("audit.html")

if __name__== "__main__":
	app.run(debug=True)

