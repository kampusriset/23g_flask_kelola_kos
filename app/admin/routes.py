import os
from flask import render_template, redirect, request, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app.utils.upload import save_image


from app import db
from app.models import User, Peraturan, Pengumuman
from app.utils.decorators import role_required

from . import admin_bp
from .forms import PenghuniForm, PeraturanForm, PengumumanForm, ProfileForm
from datetime import datetime

# === ROUTE UNTUK TEST ===
@admin_bp.route('/test-403')
def cek_halaman_error():
    abort(403)
    
@admin_bp.route('/test-404')
def cek_halaman_tidak_ditemukan():
    abort(404)
 
 
 
    
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    return render_template(
        'dashboard_admin.html',
        sidebar='partials/sidebar_admin.html',
    )




@admin_bp.route('/profile/photos', methods=['POST'])
@login_required
@role_required('admin')
def update_profile_photos():

    avatar = request.files.get('profile_photo')
    bg = request.files.get('bg_profile_photo')

    if avatar:
        current_user.profile_photo = save_image(
            file=avatar,
            old_file=current_user.profile_photo,
            folder='uploads/profile'
        )

    if bg:
        current_user.bg_profile_photo = save_image(
            file=bg,
            old_file=current_user.bg_profile_photo,
            folder='uploads/bg_profile'
        )

    if not avatar and not bg:
        flash('Tidak ada file yang diunggah', 'error')
        return redirect(url_for('admin.profile'))

    db.session.commit()
    flash('Foto profil berhasil diperbarui', 'success')
    return redirect(url_for('admin.profile'))




@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def profile():

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Data akun berhasil diperbarui', 'success')
        return redirect(url_for('admin.profile'))

    return render_template(
        'profile_admin.html',
        form=form,
        sidebar='partials/sidebar_admin.html'
    )




@admin_bp.route('/kamar', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_penghuni():
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

    return render_template(
        'kamar_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form)




@admin_bp.route('/peraturan', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def peraturan():
    form = PeraturanForm()

    if form.validate_on_submit():
        peraturan_baru = Peraturan(isi=form.isi.data)
        db.session.add(peraturan_baru)
        db.session.commit()
        flash('Peraturan berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.peraturan'))

    semua_peraturan = Peraturan.query.all()
    return render_template(
        'peraturan_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_peraturan=semua_peraturan
    )




@admin_bp.route('/hapus_peraturan/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_peraturan(id):
    peraturan = Peraturan.query.get_or_404(id)
    db.session.delete(peraturan)
    db.session.commit()
    flash('Peraturan berhasil dihapus.', 'success')
    return redirect(url_for('admin.peraturan'))




@admin_bp.route('/pengumuman', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def pengumuman():
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
        'pengumuman_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_pengumuman=semua_pengumuman,
        edit_mode=False
    )




@admin_bp.route('/pengumuman/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_pengumuman(id):
    pengumuman_edit = Pengumuman.query.get_or_404(id)
    
    form = PengumumanForm(obj=pengumuman_edit)

    if form.validate_on_submit():
        pengumuman_edit.judul = form.judul.data
        pengumuman_edit.isi = form.isi.data
        pengumuman_edit.tanggal = datetime.utcnow()
        
        db.session.commit()
        flash('Pengumuman berhasil diperbarui!', 'success')
        
        return redirect(url_for('admin.pengumuman'))

    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()


    return render_template(
        'pengumuman_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_pengumuman=semua_pengumuman,
        edit_mode=True,
        pengumuman_edit=pengumuman_edit
    )




@admin_bp.route('/hapus_pengumuman/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_pengumuman(id):
    pengumuman = Pengumuman.query.get_or_404(id)
    db.session.delete(pengumuman)
    db.session.commit()
    flash('Pengumuman berhasil dihapus.', 'success')
    return redirect(url_for('admin.pengumuman'))
