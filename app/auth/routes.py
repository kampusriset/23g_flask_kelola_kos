from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from . import auth_bp
from .forms import LoginForm, RegisterForm

# ================= LOGIN =================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            flash('Login berhasil!', 'success')

            # Redirect sesuai role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('penghuni.dashboard'))
        else:
            flash('Username atau password salah', 'danger')
    return render_template('login.html', form=form)

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
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan ke database. Coba lagi atau hubungi admin.', 'danger')

    return render_template('register.html', form=form)

# ================= LOGOUT =================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    resp = redirect(url_for('auth.login'))
    resp.delete_cookie('remember_token')
    flash('Anda telah logout.', 'info')
    return resp
