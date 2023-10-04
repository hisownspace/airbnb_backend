from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf
from .models import db, User
from .routes import spot_routes, auth_routes
from .config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)

app.register_blueprint(spot_routes, url_prefix="/api/spots")
app.register_blueprint(auth_routes, url_prefix="/api/session")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.after_request
def set_csrf_token(response):
    response.set_cookie(
        "csrf_token", generate_csrf(), samesite=None, secure=False, httponly=True
    )
    print(response)
    return response
