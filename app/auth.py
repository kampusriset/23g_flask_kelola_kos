# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login berhasil!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_pw,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Akun berhasil dibuat. Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))