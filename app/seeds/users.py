from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User

def seed_users():
    users = [
        {
            "username": "admin",
            "email": "admin@gmail.com",
            "role": "admin",
            "password": "admin123"
        },
        {
            "username": "penghuni1",
            "email": "penghuni1@gmail.com",
            "role": "penghuni",
            "password": "user123"
        }
    ]

    for u in users:
        exists = User.query.filter_by(username=u["username"]).first()
        if not exists:
            user = User(
                username=u["username"],
                email=u["email"],
                role=u["role"],
                password=generate_password_hash(u["password"])
            )
            db.session.add(user)

    db.session.commit()
    print("✅ Seed users selesai")
