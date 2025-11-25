from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# --- ROUTE LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Jika user sudah login, jangan kasih masuk halaman login lagi
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('penghuni.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # 2. Cari user berdasarkan username
        user = User.query.filter_by(username=form.username.data).first()

        # 3. Cek password hash
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            
            # Flash message kategori 'success' (akan jadi kotak hijau di HTML)
            flash(f'Selamat datang kembali, {user.username}!', 'success')
            
            # Cek apakah user mau ke halaman tertentu sebelumnya (next parameter)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            # Redirect sesuai Role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'penghuni':
                return redirect(url_for('penghuni.index'))
        else:
            # Flash message kategori 'danger' (akan jadi kotak merah di HTML)
            flash('Login gagal. Periksa username dan password Anda.', 'danger')

    return render_template('auth/login.html', form=form)


# --- ROUTE REGISTER (ADMIN) ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Jika sudah login, lempar ke dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = RegisterForm()

    if form.validate_on_submit():
        # 1. Validasi Manual: Cek Username Kembar
        if User.query.filter_by(username=form.username.data).first():
            flash('Username sudah digunakan, silakan pilih yang lain.', 'danger')
            return redirect(url_for('auth.register'))
        
        # 2. Validasi Manual: Cek Email Kembar
        if User.query.filter_by(email=form.email.data).first():
            flash('Email ini sudah terdaftar.', 'danger')
            return redirect(url_for('auth.register'))

        # 3. Hash Password (Keamanan)
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        # 4. Buat User Baru
        # PENTING: Register lewat halaman ini otomatis jadi ADMIN
        user_baru = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            role='admin' 
        )

        try:
            db.session.add(user_baru)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login dengan akun baru Anda.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan database.', 'danger')
            print(e) # Untuk debugging di terminal

    return render_template('auth/register.html', form=form)


# --- ROUTE LOGOUT ---
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('auth.login'))