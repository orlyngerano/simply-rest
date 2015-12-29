# Simple REST Implementation using python flask frameowrk
# Author Orlyn Anthony Gerano


import random, string
from flask import Flask, make_response, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

### Constants
APP_AUTH_KEY = "12345"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest.db'
db = SQLAlchemy(app)


### Model Classes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    token = db.Column(db.String(100), unique=True)

    def __init__(self, username, password, firstname, lastname, token):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.token = token

    def __repr__(self):
        return str(self.id)+","+self.username +","+ self.password+","+ self.firstname+","+ self.lastname


### Helper Functions

def _apply_app_request_filter():
	appAuthKey = request.headers.get("com.orlyngerano.rest.authkey")
	if not appAuthKey or appAuthKey!=APP_AUTH_KEY:
		abort(401)
	return

def _apply_user_request_filter():
	access_token = request.headers.get("com.orlyngerano.rest.accesstoken")
	if not access_token:
		abort(400)

	authUser = User.query.filter_by(token=access_token).first()
	if not authUser:
		abort(401)
	return

#simple random string generator
def _generate_token():
	return ''.join(random.choice(string.lowercase) for i in range(100))


def _init_db():
	db.create_all()

	username = "admin"
	password = "admin123"

	user = User.query.filter_by(username=username,password=password).first()
	
	if not user:
		user = User(username, password, "admin", "admin", _generate_token())
		db.session.add(user)
		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			pass

	return


### Error Handlers

@app.errorhandler(400)
def badRequest(error):
	return make_response(jsonify({'error':'Bad request'}),400)	

@app.errorhandler(401)
def unAuthorized(error):
	return make_response(jsonify({'error':'Unauthorized'}),401)	

@app.errorhandler(404)
def notFound(error):
	return make_response(jsonify({'error':'Not found'}),404)

@app.errorhandler(405)
def notAllowed(error):
	return make_response(jsonify({'error':'Not allowed'}),405)

@app.errorhandler(500)
def internalServerError(error):
	return make_response(jsonify({'error':'Internal Server Error'}),500)



### Initialize DB
_init_db()


### Routes
@app.route('/auth',methods=['POST'])
def auth():
	_apply_app_request_filter()

	if not request.json or not request.json.get('username') or not request.json.get('password'):
		abort(400)

	authUser = User.query.filter_by(username=request.json.get('username'),password=request.json.get('password')).first()

	if not authUser:
		abort(401)

	return jsonify({'access_token':authUser.token})  

@app.route('/user',methods=['GET'])
def getUsers():
	_apply_app_request_filter()
	_apply_user_request_filter()
	
	users = User.query.all()
	fmtUsers = []
	for user in users:
		fmtUsers.append({'username':user.username,'password':user.password,'firstname':user.firstname,'lastname':user.lastname,'token':user.token})

	return jsonify({"success":"OK", "users":fmtUsers})  

@app.route('/user/<int:userID>',methods=['GET'])
def getUser(userID):
	_apply_app_request_filter()
	_apply_user_request_filter()
	
	user = User.query.filter_by(id=userID).first()
	
	if not user:
		abort(404)

	fmtUser={'username':user.username,'password':user.password,'firstname':user.firstname,'lastname':user.lastname,'token':user.token}

	return jsonify({"success":"OK", "user":fmtUser})  


@app.route('/user',methods=['POST'])
def addUser():
	_apply_app_request_filter()
	_apply_user_request_filter()

	if not request.json or not request.json.get('username') or not request.json.get('password'):
		abort(400)

	user = User(request.json.get('username'), request.json.get('password'), "", "", _generate_token())
	if request.json.get('firstname'):
		user.firstname = request.json.get('firstname')
	if request.json.get('lastname'):
		user.lastname = request.json.get('lastname')

	db.session.add(user)
	try:
		db.session.commit()
	except exc.SQLAlchemyError:
		abort(500)

	return make_response(jsonify({'success':'Created','id':user.id}),201)


@app.route('/user/<int:userID>',methods=['PUT'])
def updateUser(userID):
	_apply_app_request_filter()
	_apply_user_request_filter()

	if not request.json:
		abort(400)

	user = User.query.filter_by(id=userID).first()

	if not user:
		abort(400)
	else:
		if request.json.get('username'):
			user.username=request.json.get('username')
		if request.json.get('password'):
			user.password=request.json.get('password')
		if request.json.get('firstname') is not None:
			user.firstname=request.json.get('firstname')
		if request.json.get('lastname') is not None:
			user.lastname=request.json.get('lastname')
		if request.json.get('access_token'):
			user.token=request.json.get('access_token')

		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			abort(500)

	return jsonify({"success":"OK"})  

@app.route('/user/<int:userID>',methods=['DELETE'])
def deleteUser(userID):
	_apply_app_request_filter()
	_apply_user_request_filter()

	user = User.query.filter_by(id=userID).first()

	if not user:
		abort(400)
	else:
		db.session.delete(user)
		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			abort(500)
	
	return jsonify({"success":"OK"})


if __name__ == '__main__':
    app.run(debug=True)
