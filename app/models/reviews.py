from sqlalchemy.sql import func
from .db import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("spots.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    review = db.Column(db.String(2000))
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    spot = db.relationship("Spot", back_populates="reviews")
    reviewer = db.relationship("User", back_populates="reviews")
    images = db.relationship("ReviewImage", back_populates="review")

    def to_dict(self, new_review=False):
        review_dict = {
            "id": self.id,
            "userId": self.user_id,
            "spotId": self.spot_id,
            "review": self.review,
            "stars": self.stars,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
        if not new_review:
            review_dict["User"] = self.reviewer.to_dict(from_review=True)
            review_dict["ReviewImages"] = [image.to_dict() for image in self.images]
        return review_dict
