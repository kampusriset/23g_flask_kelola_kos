from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask import render_template

# Inisialisasi ekstensi
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init ekstensi
    db.init_app(app)
    login_manager.init_app(app)

    # User Loader untuk Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrasi blueprint
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.penghuni import penghuni_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(penghuni_bp, url_prefix='/penghuni')
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403
    
    @app.errorhandler(404)
    def forbidden_error(error):
        return render_template('403.html'), 404

    # Route utama
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Membuat tabel jika belum ada
    with app.app_context():
        db.create_all()

    return app