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
