from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

router = Blueprint('authRouter', __name__)

class AuthRouter(MethodView):

    def __init__(self) -> None:
        super().__init__()

    def post(self):
        access_token = create_access_token(identity="example_user", fresh=True)
        return jsonify(access_token=access_token), 201

    @jwt_required()
    def get(self):
        currentUser = get_jwt_identity() # 取得jwt中的identity
        tokenContent = get_jwt() # 取得jwt中的additional_claims
        return jsonify(loggedInAs=currentUser, tokenContent=tokenContent), 200
    
router.add_url_rule('', view_func=AuthRouter.as_view('AuthRouter'))