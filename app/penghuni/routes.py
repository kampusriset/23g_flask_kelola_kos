from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app import db

from app.models import Pengumuman, Peraturan, Jadwal, Pengaduan
from app.utils.upload import save_image
from .forms import PengaduanForm, ProfileForm
from app.utils.decorators import role_required


from . import penghuni_bp


@penghuni_bp.route('/dashboard')
@login_required
@role_required('penghuni')
def dashboard():
    return render_template(
        'dashboard_penghuni.html',
        sidebar='partials/sidebar_penghuni.html'
    )




@penghuni_bp.route('/pengumuman')
@login_required
@role_required('penghuni')
def pengumuman():
    semua_pengumuman = Pengumuman.query.order_by(
        Pengumuman.tanggal.desc()
    ).all()

    return render_template(
        'pengumuman_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        semua_pengumuman=semua_pengumuman
    )




@penghuni_bp.route('/peraturan')
@login_required
@role_required('penghuni')
def peraturan():
    semua_peraturan = Peraturan.query.all()

    return render_template(
        'peraturan_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        semua_peraturan=semua_peraturan
    )





@penghuni_bp.route('/jadwal')
@login_required
@role_required('penghuni')
def jadwal():
    # Menampilkan jadwal dari yang terdekat
    semua_jadwal = Jadwal.query.filter(Jadwal.tanggal_mulai >= datetime.utcnow()).order_by(Jadwal.tanggal_mulai.asc()).all()
    return render_template('jadwal_penghuni.html', sidebar='partials/sidebar_penghuni.html', semua_jadwal=semua_jadwal)




@penghuni_bp.route('/pengaduan', methods=['GET', 'POST'])
@login_required
@role_required('penghuni')
def pengaduan():
    form = PengaduanForm()
    
    if not current_user.penghuni:
        flash('Akun Anda belum memiliki profil penghuni lengkap. Hubungi Admin.', 'danger')
        return redirect(url_for('penghuni.dashboard'))
    
    if form.validate_on_submit():
        # Ambil id penghuni yang sedang login
        laporan = Pengaduan(
            penghuni_id=current_user.penghuni.id, 
            judul=form.judul.data,
            isi=form.isi.data
        )
        db.session.add(laporan)
        db.session.commit()
        flash('Laporan Anda telah terkirim!', 'success')
        return redirect(url_for('penghuni.pengaduan'))

    # Tampilkan riwayat pengaduan milik sendiri
    riwayat = Pengaduan.query.filter_by(penghuni_id=current_user.penghuni.id).order_by(Pengaduan.tanggal.desc()).all()
    
    return render_template(
        'pengaduan_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        form=form,
        riwayat=riwayat
    )



@penghuni_bp.route('/profile/photos', methods=['POST'])
@login_required
@role_required('penghuni')
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
        return redirect(url_for('penghuni.profile'))

    db.session.commit()
    flash('Foto profil berhasil diperbarui', 'success')
    return redirect(url_for('penghuni.profile'))




@penghuni_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('penghuni')
def profile():

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Data akun berhasil diperbarui', 'success')
        return redirect(url_for('penghuni.profile'))

    return render_template(
        'profile_penghuni.html',
        form=form,
        sidebar='partials/sidebar_penghuni.html'
    )