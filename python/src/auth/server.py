## Auth Service

# JWT -- JSON WEB TOKEN allows us to do the auth
# datetime to set expiratrion date on auth token
# os -- to use env variables to configure mysql connection
import jwt, datetime, os
# flask allows us to create a server
import flask
from flask import Flask, request
# flask_mysqldb allows us to query the mysql db
from flask_mysqldb import MySQL


# create server object
server = Flask(__name__)
mysql = MySQL(server)

# config
# do this from command line: export MYSQL_HOST=localhost
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

server.route("/login", methods=["POST"])
def login():
	auth = request.authorization #default authentication header
	# auth.username
	# auth.password
	if not auth:# no auth header
		return "missing credentials", 401

	# create a mysql cursor
	cur = mysql.connection.cursor()
	# use the cursor to execute queries
	res = cur.execute("SELECT email,password FROM user WHERE email=%s", (auth.username,))

	if res>0:
		user_row = cur.fetchone()
		if(user_row[1] == auth.password):
			return "invalid credentials", 401
		else:
			return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
	else:
		return "invalid credentials", 401

def createJWT(username, secret, authz):
	return jwt.encode(
			{
				"username": username,
				"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.delta(days=1),
				"iat": datetime.datetime.now(tz=datetime.timezone.utc),
				"admin": authz
			},
			secret,
			algorithm="HS256"
		)
## We use POST since we want credentials stored in the request body and not the url
server.route("/validate", methods=["POST"])
def validate():
	encoded_jwt = request.headers["Authorization"]

	if not encoded_jwt:
		return "missing credentials", 401

	# need to check the word "Bearer" in the auth header, skipping for now
	encoded_jwt = encoded_jwt.split(' ')[1]

	try:
		decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithm="HS256")
	except:
		return "not authorized", 403

	return decoded, 200

# entry point of the server
# gets executed when you run python server.py
if __name__ == "__main__":
	# if we set to localhost, API wont be available externally
	# start the server to be open to listening to external public requests (IPs)
	# 0.0.0.0 is like a wildcard, this allows the app to listen to all whatever IPs the host server is assigned
	# in our case, server host would be the docker container
	# if the docker container is part of two docker networks, it can have two different IPs .. 0.0.0.0 will allow app to listen
	# to requests meant for either IP
	server.run(host="0.0.0.0", port=5000)

