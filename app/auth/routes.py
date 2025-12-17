from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from . import auth_bp
from .forms import LoginForm
from .forms import RegisterForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login berhasil!', 'success')

            # Redirect sesuai role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('penghuni.index'))
        else:
            flash('Username atau password salah', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # cek apakah username sudah ada
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        if existing_user_username:
            flash('Username sudah digunakan.', 'danger')
            return render_template('register.html', form=form)

        # cek apakah email sudah ada
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash('Email sudah terdaftar.', 'danger')
            return render_template('register.html', form=form)

        try:
            hashed_pw = generate_password_hash(form.password.data)
            new_admin = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_pw,
                role='admin'   # penting: set role admin
            )
            db.session.add(new_admin)
            db.session.commit()
            flash('Registrasi Admin berhasil, silakan login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan ke database. Coba lagi atau hubungi admin.', 'danger')

    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))