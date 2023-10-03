from sqlalchemy.sql import func
from .db import db


class SpotImage(db.Model):
    __tablename__ = "spot_images"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("spots.id"))
    url = db.Column(db.String(2000), nullable=False)
    preview = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    spot = db.relationship("Spot", back_populates="images")
