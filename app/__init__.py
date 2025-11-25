from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

# Inisialisasi Ekstensi
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init Ekstensi dengan app
    db.init_app(app)
    login_manager.init_app(app)

    # User Loader untuk Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrasi Blueprints
    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .penghuni.routes import penghuni_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(penghuni_bp, url_prefix='/penghuni')

    # Route halaman utama (redirect ke login)
    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Membuat tabel database (jika belum ada via SQL import)
    with app.app_context():
        # Karena Anda sudah punya file SQL, baris ini opsional
        # Tapi berguna untuk memastikan koneksi lancar
        db.create_all()

    return app
