from flask import Blueprint, request
from ..models import db, Review, Spot


review_routes = Blueprint("review_routes", __name__, url_prefix="/api/reviews")


@review_routes.route("/")
def get_all_reviews():
    all_reviews = Review.query.all()
    return {"Reviews": [review.to_dict() for review in all_reviews]}, 200
