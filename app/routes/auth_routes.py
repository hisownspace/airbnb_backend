from flask import Blueprint, request
from flask_login import login_user
from ..models import User

from ..forms import LoginForm

auth_routes = Blueprint("auth_routes", __name__, url_prefix="/api/session")


@auth_routes.route("/", methods=["POST"])
def login():
    form = LoginForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        username = form.data["username"]
        user = User.query.filter(User.username == username).first()
        login_user(user)
        return user.to_dict(), 200
    else:
        print(form.errors)
        return {"message": "Invalid credentials"}
