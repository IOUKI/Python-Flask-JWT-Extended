# blueprint test

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

def createApp():
    app = Flask(__name__)
    jwt = JWTManager()
    jwt.init_app(app)

    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)

    from routes.auth import router as authRouter
    from routes.other import router as otherRouter
    app.register_blueprint(authRouter, url_prefix='/auth')
    app.register_blueprint(otherRouter, url_prefix='/other')

    return app

app = createApp()

if __name__ == '__main__':
    app.run(debug=True)