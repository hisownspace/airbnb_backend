from sqlalchemy.sql import func
from .db import db


class ReviewImage(db.Model):
    __tablename__ = "review_images"

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id"))
    url = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    review = db.relationship("Review", back_populates="images")
