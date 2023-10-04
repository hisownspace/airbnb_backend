from sqlalchemy.sql import func
from .db import db


class Spot(db.Model):
    __tablename__ = "spots"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.DECIMAL)
    lng = db.Column(db.DECIMAL)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = db.relationship("User", back_populates="spots")
    images = db.relationship("SpotImage", back_populates="spot")
    bookings = db.relationship("Booking", back_populates="spot")
    reviews = db.relationship("Review", back_populates="spot")

    def to_dict(self):
        return {
            "id": self.id,
            "ownerId": self.owner_id,
            "address": self.address,
            "city": self.address,
            "state": self.state,
            "country": self.country,
            "lat": self.lat,
            "lng": self.lng,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "avgRating": sum([review.rating for review in self.reviews])
            / len(self.reviews)
            if len(self.reviews)
            else 1,
            "previewImage": [image.url for image in self.images if image.preview][0]
            if len(self.images)
            else None,
        }
