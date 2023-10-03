from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import spot_routes
from .config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
Migrate(app, db)

app.register_blueprint(spot_routes, url_prefix="/api/spots")


@app.route("/")
def index():
    return {"Message": "Welcome to AirBnB!"}, 200
