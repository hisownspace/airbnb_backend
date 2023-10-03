from sqlalchemy.sql import func
from .db import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("spots.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    spot = db.relationship("Spot", back_populates="bookings")
    booker = db.relationship("User", back_populates="bookings")
