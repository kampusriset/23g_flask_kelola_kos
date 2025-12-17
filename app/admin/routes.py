from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User
from app.models import User, Peraturan
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/kamar', methods=['GET', 'POST'])
@login_required
def create_penghuni():
    if current_user.role != 'admin':
        flash('Hanya admin yang bisa membuat akun penghuni.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form.get('email')
        penghuni = User(username=username, email=email, password=password, role='penghuni')
        db.session.add(penghuni)
        db.session.commit()
        flash('Akun penghuni berhasil dibuat!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('kamar.html')

@admin_bp.route('/peraturan', methods=['GET', 'POST'])
@login_required
def peraturan():
    if current_user.role != 'admin':
        flash('Hanya admin yang bisa menambahkan peraturan.', 'danger')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        isi = request.form['isi']
        if isi.strip():
            peraturan_baru = Peraturan(isi=isi)
            db.session.add(peraturan_baru)
            db.session.commit()
            flash('Peraturan berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.peraturan'))
        else:
            flash('Isi peraturan tidak boleh kosong.', 'danger')

    semua_peraturan = Peraturan.query.all()
    return render_template('peraturan.html', semua_peraturan=semua_peraturan)