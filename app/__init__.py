# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask import Flask
from app.extensions import db, login_manager
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app