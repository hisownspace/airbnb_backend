from flask import Blueprint
from ..models import Spot

spot_routes = Blueprint("spot_routes", __name__, url_prefix="/api/spots")


@spot_routes.route("/")
def get_all_spots():
    all_spots = Spot.query.all()
    return {"Spots": [spot.to_dict() for spot in all_spots]}
