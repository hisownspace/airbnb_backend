from app.models import db, User
from app import app


with app.app_context():
    user_dict = {
        "first_name": "User",
        "last_name": "One",
        "username": "user_1",
        "password": "password",
        "email": "user_1@aa.io",
    }
    new_user = User(**user_dict)
    db.session.add(new_user)
    db.session.commit()
