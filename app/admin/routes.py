import os
from flask import render_template, redirect, request, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app.utils.upload import save_image


from app import db
from app.models import User, Peraturan, Pengumuman, Kamar, Penghuni, Pengaduan, Payment
from app.utils.decorators import role_required
from app.models import User, Peraturan, Pengumuman, Jadwal # Tambahkan Jadwal di import

from . import admin_bp
from .forms import PenghuniForm, PeraturanForm, PengumumanForm, ProfileForm, KamarForm, JadwalForm
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




@admin_bp.route('/tambah-penghuni', methods=['GET', 'POST'])
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



@admin_bp.route('/kamar', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def kelola_kamar():
    form = KamarForm()
    
    
    penghuni_free = Penghuni.query.filter_by(kamar_id=None).all()
    form.penghuni_id.choices = [(0, '- Tidak Ada Penghuni -')] + [(p.id, f"{p.nama}") for p in penghuni_free]

    
    if form.validate_on_submit():
        
        if Kamar.query.filter_by(nomor_kamar=form.nomor_kamar.data).first():
            flash('Nomor kamar sudah ada!', 'danger')
        else:
            kamar = Kamar(
                nomor_kamar=form.nomor_kamar.data,
                tipe=form.tipe.data,
                harga=form.harga.data,
                status=form.status.data,
                fasilitas=form.fasilitas.data,
                keterangan=form.keterangan.data
            )
            
            if form.penghuni_id.data != 0:
                penghuni = Penghuni.query.get(form.penghuni_id.data)
                penghuni.kamar = kamar
                kamar.status = 'terisi'

            db.session.add(kamar)
            db.session.commit()
            flash('Kamar berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.kelola_kamar'))

    semua_kamar = Kamar.query.order_by(Kamar.nomor_kamar.asc()).all()

    return render_template(
        'kamar_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_kamar=semua_kamar,
        edit_mode=False,
        kamar_edit=None  
    )

@admin_bp.route('/kamar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_kamar(id):
    kamar = Kamar.query.get_or_404(id)
    form = KamarForm(obj=kamar) 
    
    penghuni_free = Penghuni.query.filter((Penghuni.kamar_id == None) | (Penghuni.kamar_id == id)).all()
    form.penghuni_id.choices = [(0, '- Tidak Ada Penghuni -')] + [(p.id, f"{p.nama}") for p in penghuni_free]

    
    current_p = Penghuni.query.filter_by(kamar_id=id).first()
    if request.method == 'GET' and current_p:
        form.penghuni_id.data = current_p.id

    if form.validate_on_submit():
        form.populate_obj(kamar) 
        
        selected_pid = form.penghuni_id.data
        
        
        if current_p and current_p.id != selected_pid:
            current_p.kamar_id = None
            
        if selected_pid != 0:
            penghuni_baru = Penghuni.query.get(selected_pid)
            penghuni_baru.kamar_id = kamar.id
            kamar.status = 'terisi'
        else:
            kamar.status = 'kosong'

        db.session.commit()
        flash('Data kamar berhasil diperbarui!', 'success')
        return redirect(url_for('admin.kelola_kamar'))

    semua_kamar = Kamar.query.order_by(Kamar.nomor_kamar.asc()).all()
    
    return render_template(
        'kamar_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_kamar=semua_kamar,
        edit_mode=True,
        kamar_edit=kamar 
    )

@admin_bp.route('/kamar/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_kamar(id):
    kamar = Kamar.query.get_or_404(id)
    
    if kamar.penghuni:
        for p in kamar.penghuni:
            p.kamar_id = None
            
    db.session.delete(kamar)
    db.session.commit()
    flash('Kamar berhasil dihapus.', 'success')
    return redirect(url_for('admin.kelola_kamar'))


@admin_bp.route('/jadwal', methods=['GET', 'POST'])
@admin_bp.route('/jadwal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def jadwal(id=None):
    jadwal_edit = None
    edit_mode = False
    
    if id:
        jadwal_edit = Jadwal.query.get_or_404(id)
        edit_mode = True
        form = JadwalForm(obj=jadwal_edit)
    else:
        form = JadwalForm()

    if form.validate_on_submit():
        if edit_mode:
            jadwal_edit.nama_kegiatan = form.nama_kegiatan.data
            jadwal_edit.tanggal_mulai = form.tanggal_mulai.data
            jadwal_edit.lokasi = form.lokasi.data
            jadwal_edit.keterangan = form.keterangan.data
            flash('Jadwal berhasil diperbarui!', 'success')
        else:
            baru = Jadwal(
                nama_kegiatan=form.nama_kegiatan.data,
                tanggal_mulai=form.tanggal_mulai.data,
                lokasi=form.lokasi.data,
                keterangan=form.keterangan.data
            )
            db.session.add(baru)
            flash('Jadwal berhasil ditambahkan!', 'success')
        
        db.session.commit()
        return redirect(url_for('admin.jadwal'))

    semua_jadwal = Jadwal.query.order_by(Jadwal.tanggal_mulai.asc()).all()
    return render_template(
        'jadwal_admin.html', 
        sidebar='partials/sidebar_admin.html', 
        form=form, 
        semua_jadwal=semua_jadwal,
        edit_mode=edit_mode,
        jadwal_edit=jadwal_edit
    )

@admin_bp.route('/jadwal/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_jadwal(id):
    item = Jadwal.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Jadwal dihapus.', 'success')
    return redirect(url_for('admin.jadwal'))
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



@admin_bp.route('/pembayaran', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def pembayaran():
    payments = Payment.query.all()

    if request.method == 'POST':
        payment_id = request.form.get('payment_id')
        payment = Payment.query.get(payment_id)

        if payment:
            payment.status = True
            db.session.commit()
            flash("Pembayaran sudah diverifikasi.", "success")
        else:
            flash("Pembayaran tidak ditemukan.", "warning")

        return redirect(url_for('admin.pembayaran'))

    return render_template('pembayaran_admin.html', 
                           payments=payments,
                           sidebar='partials/sidebar_admin.html',)