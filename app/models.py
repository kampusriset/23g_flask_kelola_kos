# MyKost Project
# MIT License (c) 2025 AnakKost Team

from app import db
from flask_login import UserMixin
from datetime import datetime
from app.extensions import db

# USERS
class User(db.Model, UserMixin):
    mykost_db = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'penghuni'), default='penghuni', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
# KAMAR
class Kamar(db.Model):
    mykost_db = 'kamar'
    id = db.Column(db.Integer, primary_key=True)
    nomor_kamar = db.Column(db.String(50), unique=True, nullable=False)
    tipe = db.Column(db.String(50))
    harga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('kosong', 'terisi'), default='kosong')
    fasilitas = db.Column(db.Text)
    keterangan = db.Column(db.Text)
    
# PENGHUNI
class Penghuni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    nama = db.Column(db.String(150), nullable=False)
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    jenis_kelamin = db.Column(db.Enum('L', 'P'))
    tanggal_masuk = db.Column(db.Date, nullable=False)
    tanggal_keluar = db.Column(db.Date)
    kamar_id = db.Column(db.Integer, db.ForeignKey('kamar.id', ondelete='SET NULL'))
    
# PEMBAYARAN
class Pembayaran(db.Model):
    mykost_db = 'pembayaran'
    id = db.Column(db.Integer, primary_key=True)
    penghuni_id = db.Column(db.Integer, db.ForeignKey('penghuni.id', ondelete='CASCADE'), nullable=False)
    kamar_id = db.Column(db.Integer, db.ForeignKey('kamar.id', ondelete='CASCADE'), nullable=False)
    bulan = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'lunas'), default='pending')
    metode = db.Column(db.String(50))
    tanggal_bayar = db.Column(db.DateTime)
    bukti_transfer = db.Column(db.String(255))

# PENGADUAN
class Pengaduan(db.Model):
    mykost_db = 'pengaduan'
    id = db.Column(db.Integer, primary_key=True)
    penghuni_id = db.Column(db.Integer, db.ForeignKey('penghuni.id', ondelete='CASCADE'), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('menunggu', 'diproses', 'selesai'), default='menunggu')
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    tanggapan = db.Column(db.Text)

# PENGUMUMAN
class Pengumuman(db.Model):
    mykost_db = 'pengumuman'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    dibuat_oleh = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

# JADWAL
class Jadwal(db.Model):
    mykost_db = 'jadwal'
    id = db.Column(db.Integer, primary_key=True)
    nama_kegiatan = db.Column(db.String(200), nullable=False)
    tanggal_mulai = db.Column(db.DateTime, nullable=False)
    tanggal_selesai = db.Column(db.DateTime)
    lokasi = db.Column(db.String(200))
    keterangan = db.Column(db.Text)
    
# PERATURAN
class Peraturan(db.Model):
    mykost_db = 'peraturan'
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    dibuat = db.Column(db.DateTime, default=datetime.utcnow)
    