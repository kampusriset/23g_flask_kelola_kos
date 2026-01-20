from datetime import datetime, date
from flask import render_template, redirect, request, url_for, flash, current_app
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app import db
import uuid
from sqlalchemy import func, extract

from app.models import Pengumuman, Peraturan, Jadwal, Pengaduan, Pembayaran
from app.utils.upload import save_image
from .forms import PengaduanForm, ProfileForm, PembayaranForm
from app.utils.decorators import role_required
import locale

from . import penghuni_bp

try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except:
    pass


@penghuni_bp.route('/dashboard')
@login_required
@role_required('penghuni')
def dashboard():
    # 1. DATA UMUM
    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.id.desc()).all()
    penghuni = current_user.penghuni
    
    # Default values
    nomor_kamar = "Belum Ada"
    sisa_hari = 0
    pembayaran_pending = 0
    
    # Variabel untuk Chart
    chart_labels = []
    chart_data_bayar = []
    aduan_stats = [0, 0, 0] # [Menunggu, Diproses, Selesai]

    if penghuni:
        # A. Info Kamar & Sisa Hari
        if penghuni.kamar:
            nomor_kamar = penghuni.kamar.nomor_kamar
        if penghuni.tanggal_keluar:
            sisa_hari = (penghuni.tanggal_keluar - date.today()).days
        
        # B. Pembayaran Pending
        pembayaran_pending = Pembayaran.query.filter_by(penghuni_id=penghuni.id, status='pending').count()

        # --- DATA CHART 1: RIWAYAT BAYAR SAYA (6 Bulan) ---
        today = date.today()
        for i in range(5, -1, -1):
            target_month = today.month - i
            target_year = today.year
            if target_month <= 0:
                target_month += 12
                target_year -= 1
            
            # Label Bulan
            chart_labels.append(date(target_year, target_month, 1).strftime('%b'))
            
            # Query Total Bayar LUNAS milik penghuni ini saja
            total = db.session.query(func.sum(Pembayaran.jumlah))\
                .filter(Pembayaran.penghuni_id == penghuni.id)\
                .filter(extract('year', Pembayaran.tanggal_bayar) == target_year)\
                .filter(extract('month', Pembayaran.tanggal_bayar) == target_month)\
                .filter(Pembayaran.status == 'lunas')\
                .scalar() or 0
            
            chart_data_bayar.append(total)

        # --- DATA CHART 2: STATISTIK PENGADUAN SAYA ---
        # Hitung jumlah pengaduan berdasarkan status
        aduan_menunggu = Pengaduan.query.filter_by(penghuni_id=penghuni.id, status='menunggu').count()
        aduan_proses   = Pengaduan.query.filter_by(penghuni_id=penghuni.id, status='diproses').count()
        aduan_selesai  = Pengaduan.query.filter_by(penghuni_id=penghuni.id, status='selesai').count()
        
        aduan_stats = [aduan_menunggu, aduan_proses, aduan_selesai]

    return render_template('dashboard_penghuni.html',
                           sidebar='partials/sidebar_penghuni.html',
                           semua_pengumuman=semua_pengumuman,
                           penghuni=penghuni,
                           nomor_kamar=nomor_kamar,
                           sisa_hari=sisa_hari,
                           pembayaran_pending=pembayaran_pending,
                           # Kirim Data Chart
                           chart_labels=chart_labels,
                           chart_data_bayar=chart_data_bayar,
                           aduan_stats=aduan_stats)




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




@penghuni_bp.route('/pembayaran', methods=['GET', 'POST'])
@login_required
def pembayaran():
    form = PembayaranForm()
    
    # 1. CEK DATA PENGHUNI & KAMAR
    penghuni = current_user.penghuni
    if not penghuni or not penghuni.kamar:
        flash('Anda belum terdaftar dalam kamar apapun. Hubungi admin.', 'danger')
        return redirect(url_for('penghuni.dashboard'))
        
    kamar = penghuni.kamar # Object kamar dari database

    # 2. AUTO-FILL DATA (Jalankan di GET maupun POST agar data tidak hilang saat error validasi)
    # Kita isi field form dengan data dari database agar aman dan konsisten
    form.nomor_kamar.data = kamar.nomor_kamar  # Masukkan string "A101" ke field nomor_kamar
    form.jumlah.data = kamar.harga           # Masukkan harga asli ke field jumlah
    
    # Set Bahasa Indonesia untuk Nama Bulan (Opsional)
    try:
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    except:
        pass # Fallback ke default sistem jika locale ID tidak ada
    
    # Set Bulan otomatis (selalu update ke bulan saat ini)
    form.bulan.data = datetime.now().strftime('%B %Y') 

    # 3. PROSES SUBMIT
    if form.validate_on_submit():
        filename = None
        metode_pilihan = form.metode.data
        
        # Validasi File Transfer
        if 'Transfer' in metode_pilihan and not form.bukti_transfer.data:
            flash('Wajib menyertakan Bukti Transfer untuk metode Transfer!', 'danger')
            return redirect(url_for('penghuni.pembayaran'))

        # Proses Upload File
        if form.bukti_transfer.data:
            file = form.bukti_transfer.data
            
            # Cek Ekstensi
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext not in {'png', 'jpg', 'jpeg'}:
                flash('Format file harus JPG atau PNG.', 'danger')
                return redirect(url_for('penghuni.pembayaran'))

            # Rename File dengan UUID agar unik
            filename = f"{uuid.uuid4().hex}.{ext}"
            
            # Pastikan folder upload ada
            upload_path = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
                
            file.save(os.path.join(upload_path, filename))

        # SIMPAN KE DATABASE
        # PENTING: Gunakan 'kamar.id' dan 'kamar.harga' dari variabel database (baris 22),
        # JANGAN ambil dari form.jumlah.data untuk menghindari manipulasi user (Inspect Element).
        new_payment = Pembayaran(
            penghuni_id=penghuni.id,
            kamar_id=kamar.id,           # ID asli (Integer)
            bulan=form.bulan.data,       # Bulan (String)
            jumlah=kamar.harga,          # Harga Asli (Integer)
            metode=metode_pilihan,
            status='pending',
            tanggal_bayar=datetime.now(),
            bukti_transfer=filename
        )

        try:
            db.session.add(new_payment)
            db.session.commit()
            flash('Pembayaran berhasil dikirim. Menunggu konfirmasi Admin.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan database.', 'danger')
            print(f"Error: {e}")

        return redirect(url_for('penghuni.pembayaran'))

    # 4. TAMPILKAN HISTORY
    data_pembayaran = Pembayaran.query.filter_by(penghuni_id=penghuni.id)\
                                      .order_by(Pembayaran.id.desc()).all()

    return render_template('pembayaran_penghuni.html', 
                           form=form, 
                           sidebar='partials/sidebar_penghuni.html',
                           pembayaran=data_pembayaran)

@penghuni_bp.route('/kamar-saya')
@login_required
@role_required('penghuni')
def kamar_saya():
    
    if not current_user.penghuni:
        flash('Data penghuni tidak ditemukan. Hubungi admin.', 'danger')
        return redirect(url_for('penghuni.dashboard'))

    my_kamar = current_user.penghuni.kamar

    return render_template(
        'kamar_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        kamar=my_kamar,
        date=date
    )