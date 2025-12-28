from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Peraturan, Pengumuman, Pengaduan
from app.utils.decorators import role_required

from . import admin_bp
from .forms import PenghuniForm, PeraturanForm, PengumumanForm
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


@admin_bp.route('/pengaduan', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def daftar_pengaduan():
    laporan_masuk = Pengaduan.query.order_by(Pengaduan.tanggal.desc()).all()
    return render_template(
        'pengaduan_admin.html',
        sidebar='partials/sidebar_admin.html',
        laporan_masuk=laporan_masuk
    )

@admin_bp.route('/pengaduan/tanggapi/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def tanggapi_pengaduan(id):
    laporan = Pengaduan.query.get_or_404(id)
    tanggapan = request.form.get('tanggapan')
    if tanggapan:
        laporan.tanggapan = tanggapan
        laporan.status = 'selesai' # Ubah status dari menunggu ke selesai
        db.session.commit()
        flash('Berhasil memberikan tanggapan!', 'success')
    return redirect(url_for('admin.daftar_pengaduan'))