from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from . import auth_bp
from .forms import LoginForm, RegisterForm

# ================= LOGIN =================

# ========================================================
# 1. ROUTE LOGIN PENGHUNI (Default: /login)
# ========================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # (Tetap gunakan logika redirect dashboard kamu yang sudah ada)
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('penghuni.dashboard'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            # TAMBAHKAN VALIDASI ROLE DISINI
            if user.role == 'admin':
                flash('Akun Admin tidak diizinkan login di sini. Silakan gunakan jalur khusus.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Jika dia penghuni, baru izinkan login
            login_user(user)
            flash('Login berhasil!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('penghuni.dashboard'))
        else:
            flash('Login gagal. Periksa username dan password.', 'danger')

    return render_template('login.html', title='Login', form=form, role='penghuni')


# ========================================================
# 2. ROUTE LOGIN ADMIN (Khusus: /login-admin)
# ========================================================
@auth_bp.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    # Kalau sudah login, lempar ke dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            # VALIDASI TAMBAHAN: Pastikan dia ADMIN
            if user.role != 'admin':
                flash('Anda bukan Admin! Silakan login di halaman penghuni.', 'danger')
                return redirect(url_for('auth.login_admin'))
                
            login_user(user)
            flash('Selamat datang Admin!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Login gagal.', 'danger')

    # PENTING: Kirim role='admin' agar tombol Daftar MUNCUL
    return render_template('login.html', title='Login Admin', form=form, role='admin')

# ================= REGISTER =================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # cek apakah username sudah ada
        if User.query.filter_by(username=form.username.data).first():
            flash('Username sudah digunakan.', 'danger')
            return render_template('register.html', form=form)

        # cek apakah email sudah ada
        if User.query.filter_by(email=form.email.data).first():
            flash('Email sudah terdaftar.', 'danger')
            return render_template('register.html', form=form)

        try:
            hashed_pw = generate_password_hash(form.password.data)
            new_admin = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_pw,
                role='admin'  # set role admin
            )
            db.session.add(new_admin)
            db.session.commit()
            flash('Registrasi Admin berhasil, silakan login.', 'success')

            return redirect(url_for('auth.login_admin'))
            
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan ke database.', 'danger')

    return render_template('register.html', form=form)

# ================= LOGOUT =================
@auth_bp.route('/logout')
@login_required
def logout():
    role_sekarang = current_user.role
    
    logout_user()
    session.clear()
    
    if role_sekarang == 'admin':
        target_url = url_for('auth.login_admin') # Balik ke Login Admin
    else:
        target_url = url_for('auth.login')       # Balik ke Login Penghuni
    
    resp = redirect(target_url)
    resp.delete_cookie('remember_token')
    flash('Anda telah logout.', 'info')
    
    return resp