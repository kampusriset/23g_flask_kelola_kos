from flask import Flask, redirect, url_for, render_template, request, flash
from werkzeug.exceptions import RequestEntityTooLarge

from .config import Config
from app.extensions import db, migrate, login_manager, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # =======================
    # Init extensions
    # =======================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'

    # =======================
    # Import models (WAJIB)
    # =======================
    from .models import User

    # =======================
    # User loader
    # =======================
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # =======================
    # Blueprint
    # =======================
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.penghuni import penghuni_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(penghuni_bp, url_prefix='/penghuni')

    # =======================
    # Error handler
    # =======================
    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        flash('Ukuran file maksimal 2MB', 'danger')
        return redirect(request.referrer or '/')

    # =======================
    # Route utama
    # =======================
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # =======================
    # Disable cache
    # =======================
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app
