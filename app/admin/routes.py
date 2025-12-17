from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Kamar
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/kamar')
@login_required
def kelola_kamar():
    # Cek apakah yang login benar-benar admin
    if current_user.role != 'admin':
        return redirect(url_for('penghuni.index'))
    
    # Ambil semua data dari tabel Kamar (SELECT * FROM kamar)
    semua_kamar = Kamar.query.all()
    
    # Kirim data 'semua_kamar' ke template 'kamar_list.html'
    return render_template('kamar_list.html', kamar=semua_kamar)

@admin_bp.route('/kamar/tambah', methods=['GET', 'POST'])
@login_required
def tambah_kamar():
    # ... (Cek role admin) ...

    if request.method == 'POST':
        # Mengambil data yang diinput user di form HTML
        nomor = request.form.get('nomor_kamar')
        tipe = request.form.get('tipe')
        harga = request.form.get('harga')
        # ... (ambil data lainnya) ...

        # Validasi sederhana: Cek apakah nomor kamar sudah ada?
        cek_kamar = Kamar.query.filter_by(nomor_kamar=nomor).first()
        if cek_kamar:
            flash('Nomor kamar sudah ada!', 'danger')
        else:
            # Membuat objek Kamar baru (persiapan insert ke DB)
            kamar_baru = Kamar(
                nomor_kamar=nomor,
                tipe=tipe,
                harga=harga,
                # ...
                status='kosong' # Default status saat dibuat
            )
            # Simpan ke database
            db.session.add(kamar_baru)
            db.session.commit()
            
            flash('Kamar berhasil ditambahkan.', 'success')
            return redirect(url_for('admin.kelola_kamar'))
            
    # Jika method GET, tampilkan form saja
    return render_template('kamar_form.html', title="Tambah Kamar")

@admin_bp.route('/kamar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_kamar(id):
    # ... (Cek role admin) ...
    
    # Cari kamar berdasarkan ID. Jika tidak ketemu, tampilkan Error 404.
    kamar = Kamar.query.get_or_404(id)

    if request.method == 'POST':
        # Timpa data lama dengan data baru dari form
        kamar.nomor_kamar = request.form.get('nomor_kamar')
        kamar.tipe = request.form.get('tipe')
        kamar.harga = request.form.get('harga')
        # ... update field lainnya ...
        
        # Simpan perubahan (UPDATE kamar SET ... WHERE id=...)
        db.session.commit()
        
        flash('Data kamar berhasil diperbarui.', 'success')
        return redirect(url_for('admin.kelola_kamar'))

    # Tampilkan form dengan data kamar yang sedang diedit
    return render_template('kamar_form.html', title="Edit Kamar", kamar=kamar)

@admin_bp.route('/kamar/hapus/<int:id>')
@login_required
def hapus_kamar(id):
    # ... (Cek role admin) ...
    
    # Cari kamar, jika ada langsung hapus
    kamar = Kamar.query.get_or_404(id)
    db.session.delete(kamar)
    db.session.commit() # Jalankan perintah DELETE di database
    
    flash('Kamar berhasil dihapus.', 'info')
    return redirect(url_for('admin.kelola_kamar'))

@admin_bp.route('/penghuni', methods=['GET', 'POST'])
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