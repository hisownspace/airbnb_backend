from flask import Blueprint, request
from flask_login import current_user

from ..forms import ImageForm, ReviewForm
from ..models import db, Review, Spot, ReviewImage


review_routes = Blueprint("review_routes", __name__, url_prefix="/api/reviews")


@review_routes.route("/current")
def get_all_user_reviews():
    all_user_reviews = current_user.reviews
    return {"Reviews": [review.to_dict() for review in all_user_reviews]}, 200


@review_routes.route("/<int:review_id>/images", methods=["POST"])
def add_image_to_review(review_id):
    form = ImageForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        review = Review.query.get(review_id)
        if not review:
            return {"message": "Review couldn't be found"}, 404
        if len(review.images) >= 10:
            return {
                "message": "Maximum number of images for this resource was reached"
            }, 403
        new_review_image = ReviewImage(url=form.data["url"])
        new_review_image.review = review
        db.session.add(new_review_image)
        db.session.commit()
        return new_review_image.to_dict(), 200
    else:
        return {"message": "Error validations", "errors": form.errors}, 400


@review_routes.route("/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    form = ReviewForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        data = {
            "review": form.data["review"],
            "stars": form.data["stars"],
        }
        review_data = Review.query.filter(Review.id == review_id)
        review = review_data.first()
        if not review:
            return {"message": "Review couldn't be found"}, 404
        review_data.update(data)
        db.session.commit()
        return review.to_dict(new_review=True), 201
    return {"message": "Bad Request", "errors": form.errors}, 400


@review_routes.route("/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"message": "Review couldn't be found"}, 400

    db.session.delete(review)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
