from flask import Blueprint, request
from flask_login import login_required, logout_user, current_user

from ..forms import SpotForm
from ..models import db, Spot

spot_routes = Blueprint("spot_routes", __name__, url_prefix="/api/spots")


@spot_routes.route("/")
@login_required
def get_all_spots():
    all_spots = Spot.query.all()
    return {"Spots": [spot.to_dict() for spot in all_spots]}, 200


@spot_routes.route("/current")
def get_current_user_spots():
    return {"Spots": [spot.to_dict() for spot in current_user.spots]}, 200


@spot_routes.route("/<int:spot_id>")
def get_single_spot(spot_id):
    spot = Spot.query.get(spot_id)
    if spot:
        return spot.to_dict(), 200
    else:
        return {"message": "Spot couldn't be found."}, 404


@spot_routes.route("/", methods=["POST"])
def create_spot():
    form = SpotForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        data = {
            "address": form.data["address"],
            "city": form.data["city"],
            "state": form.data["state"],
            "country": form.data["country"],
            "lat": form.data["lat"],
            "lng": form.data["lng"],
            "name": form.data["name"],
            "description": form.data["description"],
            "price": form.data["price"],
            "owner": current_user,
        }
        new_spot = Spot(**data)
        db.session.add(new_spot)
        db.session.commit()
        return new_spot.to_dict(), 201
    return {"message": "Bad Request", "errors": form.errors}, 400
