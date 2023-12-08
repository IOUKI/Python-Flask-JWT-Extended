from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

router = Blueprint('otherRouter', __name__)

class OtherRouter(MethodView):

    def __init__(self) -> None:
        super().__init__()

    @jwt_required()
    def get(self):
        currentUser = get_jwt_identity() # 取得jwt中的identity
        tokenContent = get_jwt() # 取得jwt中的additional_claims
        return jsonify(loggedInAs=currentUser, tokenContent=tokenContent), 200
    
router.add_url_rule('', view_func=OtherRouter.as_view('OtherRouter'))