from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
jwt = JWTManager(app)


# We verify the users password here, so we are returning a fresh access token
@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user", fresh=True)
    return jsonify(access_token=access_token)


# If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
@app.route("/logout", methods=["POST"])
@jwt_required()
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@app.route("/protected", methods=["GET"])
@jwt_required(fresh=True)
def protected():
    currentUser = get_jwt_identity() # 取得jwt中的identity
    tokenContent = get_jwt() # 取得jwt中的additional_claims
    return jsonify(loggedInAs=currentUser, tokenContent=tokenContent), 200

@app.route('/notFresh', methods=['GET'])
@jwt_required()
def notFresh():
    currentUser = get_jwt_identity() # 取得jwt中的identity
    tokenContent = get_jwt() # 取得jwt中的additional_claims
    return jsonify(loggedInAs=currentUser, tokenContent=tokenContent), 200


if __name__ == "__main__":
    app.run()