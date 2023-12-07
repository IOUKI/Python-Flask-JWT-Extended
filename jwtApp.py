from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)
jwt = JWTManager()

app.config['JWT_SECRET_KEY'] = 'jingzesystem'
jwt.init_app(app)

# 登入: 回傳前端token
@app.route('/login', methods=['POST'])
def login(): 

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != 'test' or password != 'test': 
        return jsonify({"msg": "Bad username or password"}), 401

    tokenContent = {
        'account': username,
        'password': password
    }
    access_token = create_access_token(identity=username, additional_claims=tokenContent) # identity: 存放識別使用者的訊息，例如ID ,additional_claims: 存放額外的訊息資料
    return jsonify(access_token=access_token), 200
    
# 驗證token
@app.route('/protected', methods=['GET', 'POST'])
@jwt_required(optional=True) # optional: 如果jwt不存在，get_jwt_identity() ,get_jwt() 會回傳None
def protected():
    currentUser = get_jwt_identity() # 取得jwt中的identity
    tokenContent = get_jwt() # 取得jwt中的additional_claims
    return jsonify(loggedInAs=currentUser, tokenContent=tokenContent), 200

@app.route("/only_headers")
@jwt_required(locations=["headers"]) # locations: 指定夾帶token的位置，此處範例為headers
def only_headers():
    return jsonify(foo="baz")

if __name__ == '__main__':
    app.run(debug=True)