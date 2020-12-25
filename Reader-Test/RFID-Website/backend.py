from flask import Flask, request, render_template
from MongoController import DBClient
from ZugangsKontrolle import Zugang

#Maybe to delete packages
#import json
#import sys

app = Flask(__name__)
zugang = Zugang()
dbClient = DBClient()

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/auth', methods=['GET'])
def auth():
	auth = zugang.authorizedWrapper()
	if auth:
		return db()
	else:
		return "Access denied"
@app.route('/accounts', methods=['POST'])
def addAccount():
	auth = zugang.authorizedWrapper()
	if auth:
		dbClient.pws().insert_one(request.json)
		return "Account added"
	else:
		return "No Authorization yet. Return to Landing Page please."

def db():
	documents ={}
	
	table = """<table >
  		<tr>
    	<th>Account</th>
    	<th>Password</th> 
  		</tr>"""

	for acc in dbClient.pws().find():
		table+= "<tr><td>"+acc["name"]+"</td><td>"+acc["pw"]+"</td></tr>"
	
	table+="</table>"
	return table
	



