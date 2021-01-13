from flask import Flask, request, render_template
from MongoController import DBClient
from ZugangsKontrolle import Zugang

app = Flask(__name__)
zugang = Zugang()
dbClient = DBClient()

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/settings', methods=['GET'])
def settings():
	return render_template("settings.html")

#
#	AUTHORIZATION
#

@app.route('/auth', methods=['GET'])
def auth():
	auth = zugang.authorizedWrapper()
	if auth:
		table = dbClient.pws().find()
		return render_template("access.html", dbcontent=table)
	else:
		return "Access denied"
#
#	ACCOUNT MANAGEMENT
#
@app.route('/auth/accounts', methods=['POST'])
def addAccount():
	auth = zugang.authorizedWrapper()
	if auth:
		name = request.form["name"]
		pw = request.form["pw"]
		dbClient.pws().insert_one({"name": name, "pw": pw})
		
		table = dbClient.pws().find()
		return render_template("access.html", dbcontent=table)
	else:
		return "No Authorization yet. Return to Landing Page please."

@app.route('/auth/accountsDEL', methods=['POST'])	#Should be DELETE instead of POST but HTML forms does not support DELETE
def delAccount():
	auth = zugang.authorizedWrapper()
	if auth:
		name = request.form["name"]
		dbClient.pws().delete_one({"name": name})
	
		table = dbClient.pws().find()
		return render_template("access.html", dbcontent=table)
	else:
		return "No Authorization yet. Return to Landing Page please."

#
#	CARD-DATA-MANAGEMENT
#	
@app.route('/cardPW', methods=['POST'])	#Should be PUT but HTML does not support
def changePassword():
	auth = zugang.authorizedWrapper()
	if auth:
		data = request.form	#PUT CORRECT DATA INSIDE
		converted = strToInt(data["password"])
		print(converted)
		if len(converted) == 16 and all(isinstance(x, int) for x in converted):
			zugang.changePassword(converted)
			return render_template("settings.html", rdy = "Password successfully changed.")
		else:
			return "wrong input"
	else:
		return "Not authorized."

@app.route('/cardKey', methods=['POST'])
def changeKey():
	auth = zugang.authorizedWrapper()
	if auth:
		data = request.form	#PUT CORRECT DATA INSIDE
		converted = strToInt(data["key"])

		if len(converted) == 16 and all(isinstance(x, int) for x in converted):
			zugang.changeKey(converted)
			return render_template("settings.html", rdy = "Key successfully changed.")			
		else:
			return "wrong input"
	else:
		return "Not authorized."

def strToInt(string):
	splitted = string.split(" ")
	data = []
	for item in splitted:
		data.append(int(item))
	return data

