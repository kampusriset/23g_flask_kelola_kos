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
    # 1. Cek Role (Keamanan)
    if current_user.role != 'admin':
        flash('Hanya admin yang bisa mengakses halaman ini.', 'danger')
        return redirect(url_for('admin.dashboard'))

    form = PengumumanForm()

    # 2. Logic BUAT BARU (Create)
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

    # 3. Ambil data list untuk tampilan kanan
    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()

    # 4. Render halaman biasa (Mode Edit: False)
    return render_template(
        'pengumuman.html',
        form=form,
        semua_pengumuman=semua_pengumuman,
        edit_mode=False
    )


@admin_bp.route('/pengumuman/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pengumuman(id):
    # 1. Cek Role (Keamanan)
    if current_user.role != 'admin':
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # 2. Ambil data yang mau diedit
    pengumuman_edit = Pengumuman.query.get_or_404(id)
    
    # Isi form dengan data lama (Pre-fill)
    form = PengumumanForm(obj=pengumuman_edit)

    # 3. Logic SIMPAN PERUBAHAN (Update)
    if form.validate_on_submit():
        pengumuman_edit.judul = form.judul.data
        pengumuman_edit.isi = form.isi.data
        # Tanggal update opsional: pengumuman_edit.tanggal = datetime.utcnow()
        
        db.session.commit()
        flash('Pengumuman berhasil diperbarui!', 'success')
        
        # Setelah sukses, kembali ke halaman utama (reset form jadi kosong)
        return redirect(url_for('admin.pengumuman'))

    # 4. Ambil data list untuk tampilan kanan (PENTING! Agar list tetap muncul saat mode edit)
    semua_pengumuman = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()

    # 5. Render halaman YANG SAMA, tapi aktifkan Mode Edit
    return render_template(
        'pengumuman.html',
        form=form,
        semua_pengumuman=semua_pengumuman,
        edit_mode=True,             # <--- Memicu tampilan form berubah jadi 'Edit'
        pengumuman_edit=pengumuman_edit # <--- Untuk highlight kartu di list kanan
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
