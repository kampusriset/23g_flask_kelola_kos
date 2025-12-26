from flask import app, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User
from app.models import User, Peraturan
from app.models import Pengumuman
from . import admin_bp
from .forms import PenghuniForm, PeraturanForm, PengumumanForm

# === ROUTE UNTUK TEST ===
@admin_bp.route('/test-403')
def cek_halaman_error():
    abort(403)
    
@admin_bp.route('/test-404')
def cek_halaman_tidak_ditemukan():
    abort(404)
    
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

    form = PenghuniForm()

    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        penghuni = User(
            username=form.username.data,
            email=form.email.data,
            password=password,
            role='penghuni'
        )
        db.session.add(penghuni)
        db.session.commit()
        flash('Akun penghuni berhasil dibuat!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('kamar.html', form=form)




@admin_bp.route('/peraturan', methods=['GET', 'POST'])
@login_required
def peraturan():
    if current_user.role != 'admin':
        flash('Hanya admin yang bisa menambahkan peraturan.', 'danger')
        return redirect(url_for('admin.dashboard'))

    form = PeraturanForm()

    if form.validate_on_submit():
        peraturan_baru = Peraturan(isi=form.isi.data)
        db.session.add(peraturan_baru)
        db.session.commit()
        flash('Peraturan berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.peraturan'))

    semua_peraturan = Peraturan.query.all()
    return render_template(
        'peraturan.html',
        form=form,
        semua_peraturan=semua_peraturan
    )




@admin_bp.route('/hapus_peraturan/<int:id>', methods=['POST'])
@login_required
def hapus_peraturan(id):
    peraturan = Peraturan.query.get_or_404(id)
    db.session.delete(peraturan)
    db.session.commit()
    flash('Peraturan berhasil dihapus.', 'success')
    return redirect(url_for('admin.peraturan'))




@admin_bp.route('/pengumuman', methods=['GET', 'POST'])
@login_required
def pengumuman():
    if current_user.role != 'admin':
        flash('Hanya admin yang bisa menambahkan pengumuman.', 'danger')
        return redirect(url_for('admin.dashboard'))

    form = PengumumanForm()

    if form.validate_on_submit():
        pengumuman_baru = Pengumuman(
            judul=form.judul.data,
            isi=form.isi.data,
            dibuat_oleh=current_user.id
        )
        db.session.add(pengumuman_baru)
        db.session.commit()
        flash('Pengumuman berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.pengumuman'))

    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    return render_template(
        'pengumuman.html',
        form=form,
        semua_pengumuman=semua_pengumuman
    )




@admin_bp.route('/edit_pengumuman/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pengumuman(id):
    pengumuman = Pengumuman.query.get_or_404(id)
    form = PengumumanForm(obj=pengumuman)

    if form.validate_on_submit():
        pengumuman.judul = form.judul.data
        pengumuman.isi = form.isi.data
        db.session.commit()
        flash('Pengumuman berhasil diperbarui!', 'success')
        return redirect(url_for('admin.pengumuman'))

    return render_template(
        'edit_pengumuman.html',
        form=form,
        pengumuman=pengumuman
    )




# ✅ Route Hapus Pengumuman
@admin_bp.route('/hapus_pengumuman/<int:id>', methods=['POST'])
@login_required
def hapus_pengumuman(id):
    pengumuman = Pengumuman.query.get_or_404(id)
    db.session.delete(pengumuman)
    db.session.commit()
    flash('Pengumuman berhasil dihapus.', 'success')
    return redirect(url_for('admin.pengumuman'))
