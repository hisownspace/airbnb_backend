from flask import Blueprint, request
from flask_login import login_required, logout_user, current_user

from ..forms import SpotForm, ImageForm, ReviewForm
from ..models import db, Spot, SpotImage, Review

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
        return spot.to_dict(single=True), 200
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


@spot_routes.route("/<int:spot_id>", methods=["PUT"])
def update_spot(spot_id):
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
        }
        spot_data = Spot.query.filter(Spot.id == spot_id)
        spot = spot_data.first()
        if not spot:
            return {"message": "Spot couldn't be found"}, 404
        spot_data.update(data)
        db.session.commit()
        return spot.to_dict(), 201
    return {"message": "Bad Request", "errors": form.errors}, 400


@spot_routes.route("/<int:spot_id>", methods=["DELETE"])
def delete_spot(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return {"message": "Spot couldn't be found"}, 404
    db.session.delete(spot)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200


@spot_routes.route("/<int:spot_id>/images", methods=["POST"])
def add_image_to_spot(spot_id):
    form = ImageForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        spot = Spot.query.get(spot_id)
        if not spot:
            return {"message": "Spot couldn't be found"}, 404

        data = {"url": form.data["url"], "preview": form.data["preview"]}

        new_image = SpotImage(**data)
        new_image.spot = spot

        db.session.add(new_image)
        db.session.commit()
        return new_image.to_dict(), 200
    return {"message": "Invalid request", "errors": form.errors}, 401


@spot_routes.route("/<int:spot_id>/reviews")
def get_all_spot_reviews(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return {"message": "Spot couldn't be found"}, 404
    else:
        return {"Reviews": [review.to_Dict() for review in spot.reviews]}, 200
    spot = Spot.query.get(spot_id)
    if not spot:
        return {"message": "Spot couldn't be found"}, 404
    else:
        return {"Reviews": [review.to_Dict() for review in spot.reviews]}, 200


@spot_routes.route("/<int:spot_id>/reviews", methods=["POST"])
def create_review(spot_id):
    form = ReviewForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        spot = Spot.query.get(spot_id)
        if not spot:
            return {"message": "Spot couldn't be found"}, 404
        data = {"review": form.data["review"], "stars": form.data["stars"]}
        new_review = Review(**data)
        new_review.reviewer = current_user
        new_review.spot = spot
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict(new_review=True), 201
    return {"message": "Bad Request", "errors": form.errors}, 400
