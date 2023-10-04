from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships

    spots = db.relationship("Spot", back_populates="owner")
    bookings = db.relationship("Booking", back_populates="booker")
    reviews = db.relationship("Review", back_populates="reviewer")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, val):
        return check_password_hash(self.password, val)

    def to_dict(self, from_review=False):
        if from_review:
            return {
                "id": self.id,
                "firstName": self.first_name,
                "lastName": self.last_name,
            }
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "username": self.username,
        }
