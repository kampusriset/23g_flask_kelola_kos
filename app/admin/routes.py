import os
from flask import render_template, redirect, request, url_for, flash, abort, current_app, send_from_directory
from flask_login import login_required, current_user
from app.utils.upload import save_image
from sqlalchemy import extract, func


from app import db
from app.models import User, Peraturan, Pengumuman, Kamar, Penghuni, Pengaduan, Pembayaran, Jadwal
from app.utils.decorators import role_required

from . import admin_bp
from .forms import PengaduanForm, PeraturanForm, PengumumanForm, ProfileForm, KamarForm, JadwalForm, UnifiedPenghuniForm, TanggapanForm
from datetime import datetime, date, timedelta

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
    # --- 1. DATA LAMA (JANGAN DIHAPUS) ---
    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.id.desc()).all()
    total_kamar = Kamar.query.count()
    kamar_terisi = Kamar.query.filter_by(status='terisi').count()
    kamar_kosong = total_kamar - kamar_terisi
    total_penghuni = Penghuni.query.count()
    pembayaran_pending = Pembayaran.query.filter_by(status='pending').count()

    # --- 2. DATA BARU UNTUK CHART (TAMBAHKAN INI) ---
    
    # A. Data Grafik Pendapatan 6 Bulan Terakhir
    chart_labels = [] 
    chart_income = []
    today = date.today()

    # Loop 5 bulan ke belakang sampai bulan ini
    for i in range(5, -1, -1):
        # Logika mundur bulan
        target_month = today.month - i
        target_year = today.year
        if target_month <= 0:
            target_month += 12
            target_year -= 1
        
        # Nama Bulan (Singkat)
        nama_bulan = date(target_year, target_month, 1).strftime('%b') # Jan, Feb, Mar
        chart_labels.append(nama_bulan)

        # Query Total Duit (LUNAS saja)
        total = db.session.query(func.sum(Pembayaran.jumlah))\
            .filter(extract('year', Pembayaran.tanggal_bayar) == target_year)\
            .filter(extract('month', Pembayaran.tanggal_bayar) == target_month)\
            .filter(Pembayaran.status == 'lunas')\
            .scalar() or 0
        
        chart_income.append(total)

    return render_template('dashboard_admin.html',
                           sidebar='partials/sidebar_admin.html',
                           semua_pengumuman=semua_pengumuman,
                           total_kamar=total_kamar,
                           kamar_terisi=kamar_terisi,
                           kamar_kosong=kamar_kosong,
                           total_penghuni=total_penghuni,
                           pembayaran_pending=pembayaran_pending,
                           # KIRIM DATA CHART KE HTML
                           chart_labels=chart_labels,
                           chart_income=chart_income)




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




# 1. READ (LIST) & CREATE
@admin_bp.route('/penghuni', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def kelola_penghuni():
    form = UnifiedPenghuniForm()
    
    # LOGIC: CREATE DATA BARU
    if form.validate_on_submit():
        if not form.password.data:
            flash('Password wajib diisi untuk penghuni baru!', 'danger')
        else:
            # 1. Buat User
            user_baru = User(
                username=form.username.data,
                email=form.email.data,
                role='penghuni'
            )
            user_baru.set_password(form.password.data)
            db.session.add(user_baru)
            db.session.flush() # Ambil ID

            # 2. Buat Penghuni
            penghuni_baru = Penghuni(
                user_id=user_baru.id,
                nama=form.nama_lengkap.data,
                no_hp=form.no_hp.data,
                jenis_kelamin=form.jenis_kelamin.data,
                tanggal_masuk=form.tanggal_masuk.data,
                alamat=form.alamat.data
            )
            db.session.add(penghuni_baru)
            db.session.commit()
            flash('Penghuni berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.kelola_penghuni'))

    semua_penghuni = Penghuni.query.order_by(Penghuni.tanggal_masuk.desc()).all()
    
    return render_template(
        'penghuni_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_penghuni=semua_penghuni,
        edit_mode=False,
        penghuni_edit=None
    )




@admin_bp.route('/penghuni/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_penghuni(id):
    penghuni_edit = Penghuni.query.get_or_404(id)
    user_terkait = penghuni_edit.user
    
    # Isi form dengan data lama (User + Penghuni)
    form = UnifiedPenghuniForm(obj=penghuni_edit)
    
    # Pre-populate data dari tabel User jika request GET
    if request.method == 'GET':
        form.username.data = user_terkait.username
        form.email.data = user_terkait.email
        # Map field nama penghuni (krn di form namanya nama_lengkap, di model namanya nama)
        form.nama_lengkap.data = penghuni_edit.nama

    # LOGIC: SIMPAN PERUBAHAN
    if form.validate_on_submit():
        # Update User
        user_terkait.username = form.username.data
        user_terkait.email = form.email.data
        if form.password.data: # Hanya update password jika diisi
            user_terkait.set_password(form.password.data)
            
        # Update Penghuni
        penghuni_edit.nama = form.nama_lengkap.data
        penghuni_edit.no_hp = form.no_hp.data
        penghuni_edit.jenis_kelamin = form.jenis_kelamin.data
        penghuni_edit.tanggal_masuk = form.tanggal_masuk.data
        penghuni_edit.alamat = form.alamat.data
        
        db.session.commit()
        flash('Data penghuni diperbarui!', 'success')
        return redirect(url_for('admin.kelola_penghuni'))

    semua_penghuni = Penghuni.query.order_by(Penghuni.tanggal_masuk.desc()).all()

    return render_template(
        'penghuni_admin.html',
        sidebar='partials/sidebar_admin.html',
        form=form,
        semua_penghuni=semua_penghuni,
        edit_mode=True,
        penghuni_edit=penghuni_edit
    )




@admin_bp.route('/penghuni/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_penghuni(id):
    penghuni = Penghuni.query.get_or_404(id)
    user_id = penghuni.user_id
    User.query.filter_by(id=user_id).delete() # Cascade hapus penghuni
    db.session.commit()
    flash('Data penghuni dihapus.', 'success')
    return redirect(url_for('admin.kelola_penghuni'))




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

                # --- PERBAIKAN: Tambahkan logic set tanggal keluar di sini ---
                if not penghuni.tanggal_keluar:
                     penghuni.tanggal_keluar = date.today() + timedelta(days=30)

                     #testing 
                     #penghuni.tanggal_keluar = datetime.now() + timedelta(seconds=30)
                # -------------------------------------------------------------

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
        kamar_edit=None,
        date=date
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
            
            # --- PERBAIKAN: Ganti jatuh_tempo jadi tanggal_keluar ---
            if not penghuni_baru.tanggal_keluar:
                penghuni_baru.tanggal_keluar = date.today() + timedelta(days=30)

                #penghuni_baru.tanggal_keluar = datetime.now() + timedelta(seconds=30)
            # --------------------------------------------------------
            
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
        kamar_edit=kamar,
        date=date
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



@admin_bp.route('/kamar/perpanjang/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def perpanjang_sewa(id):
    # Kita cari kamar berdasarkan ID
    kamar = Kamar.query.get_or_404(id)
    
    # Cek apakah ada penghuninya
    if kamar.penghuni:
        # Loop karena relasi penghuni di html kamu pakai loop (walau biasanya 1 kamar 1 orang)
        for p in kamar.penghuni:
            # Jika tanggal_keluar kosong, kita set dari hari ini
            if not p.tanggal_keluar:
                p.tanggal_keluar = date.today()
            
            # LOGIC UTAMA: Tambah 30 hari dari tanggal_keluar yang sekarang
            p.tanggal_keluar = p.tanggal_keluar + timedelta(days=30)

            #p.tanggal_keluar = p.tanggal_keluar + timedelta(seconds=30)
            
        db.session.commit()
        flash('Masa sewa berhasil diperpanjang 30 hari!', 'success')
    else:
        flash('Kamar ini kosong, tidak bisa diperpanjang.', 'warning')
        
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



# =========================
# Route: Lihat Daftar Pengaduan
# =========================
@admin_bp.route('/pengaduan', methods=['GET'])
@login_required
@role_required('admin')
def pengaduan():
    # Ambil semua data urut terbaru
    laporan_masuk = Pengaduan.query.order_by(Pengaduan.tanggal.desc()).all()
    
    # Form kosong untuk CSRF token di setiap item loop
    form = TanggapanForm()

    # --- LOGIKA MANUAL ATTACHMENT (Jika belum ada relasi di models) ---
    for l in laporan_masuk:
        # Cari Penghuni
        p_asli = Penghuni.query.get(l.penghuni_id)
        if p_asli:
            l.penghuni = p_asli
            # Cari Kamar
            if p_asli.kamar_id:
                l.penghuni.kamar = Kamar.query.get(p_asli.kamar_id)
            else:
                l.penghuni.kamar = None
        else:
            # Data Dummy
            l.penghuni = type('obj', (object,), {'nama': 'User Terhapus', 'kamar': None})
    # ------------------------------------------------------------------

    return render_template(
        'pengaduan_admin.html',
        sidebar='partials/sidebar_admin.html',
        laporan_masuk=laporan_masuk,
        form=form
    )

# =========================
# Route: Ubah Status ke DIPROSES
# =========================
@admin_bp.route('/pengaduan/proses/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def proses_pengaduan(id):
    # Ambil data pengaduan
    laporan = Pengaduan.query.get_or_404(id)
    
    # Hanya bisa diproses jika statusnya masih 'menunggu'
    if laporan.status == 'menunggu':
        laporan.status = 'diproses'
        db.session.commit()
        flash('Status pengaduan diubah menjadi DIPROSES.', 'info')
    
    return redirect(url_for('admin.pengaduan'))

# =========================
# Route: Hapus Pengaduan
# =========================
@admin_bp.route('/pengaduan/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def hapus_pengaduan(id):
    laporan = Pengaduan.query.get_or_404(id)
    db.session.delete(laporan)
    db.session.commit()
    flash('Laporan pengaduan berhasil dihapus.', 'success')
    return redirect(url_for('admin.pengaduan'))

# =========================
# Route: Proses Tanggapan (POST Only)
# =========================
@admin_bp.route('/pengaduan/tanggapi/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def tanggapi_pengaduan(id):
    form = TanggapanForm()
    
    # Ambil data pengaduan
    laporan = Pengaduan.query.get_or_404(id)

    if form.validate_on_submit():
        laporan.tanggapan = form.tanggapan.data
        laporan.status = 'selesai'
        db.session.commit()
        flash('Tanggapan berhasil dikirim dan status diperbarui!', 'success')
    else:
        flash('Gagal mengirim tanggapan. Pastikan isi tidak kosong.', 'danger')

    return redirect(url_for('admin.pengaduan'))



# =======================================================
# 1. ROUTE LIST PEMBAYARAN (ADMIN)
# =======================================================
@admin_bp.route('/pembayaran')
@login_required
@role_required('admin')
def pembayaran():
    # 1. Ambil semua data pembayaran urut dari yang terbaru
    data_pembayaran = Pembayaran.query.order_by(Pembayaran.id.desc()).all()

    # 2. LOGIKA MANUAL ATTACHMENT (PENTING!)
    # Karena di models Pembayaran tidak ada relationship, kita cari manual datanya
    # dan kita tempelkan ke object pembayaran agar bisa dibaca HTML.
    
    for p in data_pembayaran:
        # --- Cari Data Penghuni ---
        # Menggunakan p.penghuni_id (Integer) dari model kamu
        p_asli = Penghuni.query.get(p.penghuni_id)
        if p_asli:
            p.penghuni = p_asli
        else:
            # Dummy Data jika penghuni sudah dihapus
            p.penghuni = type('obj', (object,), {
                'nama': 'Penghuni Terhapus', 
                'no_hp': '-'
            })

        # --- Cari Data Kamar ---
        # Menggunakan p.kamar_id (Integer) dari model kamu
        k_asli = Kamar.query.get(p.kamar_id)
        if k_asli:
            p.kamar = k_asli
        else:
            # Dummy Data jika kamar sudah dihapus
            p.kamar = type('obj', (object,), {
                'nomor_kamar': 'Unknown', 
                'tipe': '-'
            })

    return render_template('pembayaran_admin.html', 
                           payments=data_pembayaran,
                           sidebar='partials/sidebar_admin.html')


# =======================================================
# 2. ROUTE AKSI VERIFIKASI (+30 HARI)
# =======================================================
@admin_bp.route('/pembayaran/konfirmasi/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def konfirmasi_pembayaran(id):
    # Ambil data pembayaran
    bayar = Pembayaran.query.get_or_404(id)
    
    # Validasi Status
    if bayar.status == 'lunas':
        flash('Pembayaran ini sudah dikonfirmasi sebelumnya.', 'warning')
        return redirect(url_for('admin.pembayaran'))
    
    # A. Ubah Status Pembayaran
    bayar.status = 'lunas'
    
    # B. Set Tanggal Bayar (jika belum ada)
    if not bayar.tanggal_bayar:
        bayar.tanggal_bayar = datetime.now()
    
    # C. LOGIKA TAMBAH MASA SEWA 30 HARI
    # Cari penghuni manual menggunakan ID dari tabel Pembayaran
    penghuni = Penghuni.query.get(bayar.penghuni_id)
    
    if penghuni:
        # Jika tanggal keluar kosong atau sudah lewat hari ini (kadaluarsa)
        if not penghuni.tanggal_keluar or penghuni.tanggal_keluar < date.today():
            # Reset hitungan mulai hari ini
            penghuni.tanggal_keluar = date.today()
            
        # Tambahkan 30 hari kedepan
        penghuni.tanggal_keluar = penghuni.tanggal_keluar + timedelta(days=30)
        
        pesan = f"Verifikasi Sukses! Masa sewa {penghuni.nama} diperpanjang sampai {penghuni.tanggal_keluar.strftime('%d-%m-%Y')}."
    else:
        pesan = "Pembayaran diverifikasi, tetapi data Penghuni tidak ditemukan (mungkin sudah dihapus)."

    db.session.commit()
    flash(pesan, 'success')
    
    return redirect(url_for('admin.pembayaran'))


# =======================================================
# 3. ROUTE CETAK INVOICE
# =======================================================
@admin_bp.route('/pembayaran/invoice/<int:id>')
@login_required
def cetak_invoice(id):
    pembayaran = Pembayaran.query.get_or_404(id)
    
    # Validasi: Hanya boleh cetak yang LUNAS
    if pembayaran.status != 'lunas':
        flash('Invoice hanya tersedia untuk pembayaran yang sudah LUNAS.', 'warning')
        if current_user.role == 'admin':
            return redirect(url_for('admin.pembayaran'))
        else:
            return redirect(url_for('penghuni.pembayaran'))

    # LOGIKA MANUAL ATTACHMENT (Sama seperti di atas)
    # Agar template invoice tidak error saat panggil {{ p.penghuni.nama }}
    
    # 1. Attach Penghuni
    p_asli = Penghuni.query.get(pembayaran.penghuni_id)
    if p_asli:
        pembayaran.penghuni = p_asli
    else:
        pembayaran.penghuni = type('obj', (object,), {'nama': 'Penghuni Tidak Dikenal', 'no_hp': '-'})

    # 2. Attach Kamar
    k_asli = Kamar.query.get(pembayaran.kamar_id)
    if k_asli:
        pembayaran.kamar = k_asli
    else:
        pembayaran.kamar = type('obj', (object,), {'nomor_kamar': '-', 'tipe': '-'})

    return render_template('invoice_print.html', p=pembayaran)


# =======================================================
# 4. ROUTE LIHAT BUKTI FOTO
# =======================================================
@admin_bp.route('/lihat-bukti/<filename>')
@login_required
def lihat_bukti(filename):
    folder_private = current_app.config['UPLOAD_FOLDER']
    try:
        return send_from_directory(folder_private, filename)
    except FileNotFoundError:
        abort(404)