from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'penghuni'), default='penghuni', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi ke data profil penghuni (One-to-One)
    data_penghuni = db.relationship('Penghuni', backref='akun', uselist=False)

class Kamar(db.Model):
    __tablename__ = 'kamar'
    id = db.Column(db.Integer, primary_key=True)
    nomor_kamar = db.Column(db.String(50), unique=True, nullable=False)
    tipe = db.Column(db.String(50))
    harga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('kosong', 'terisi'), default='kosong')
    fasilitas = db.Column(db.Text)
    keterangan = db.Column(db.Text)

    # Relasi: Satu kamar bisa punya riwayat banyak penghuni (atau satu aktif)
    riwayat_penghuni = db.relationship('Penghuni', backref='kamar')

class Penghuni(db.Model):
    __tablename__ = 'penghuni'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    nama = db.Column(db.String(150), nullable=False)
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    jenis_kelamin = db.Column(db.Enum('L', 'P'))
    tanggal_masuk = db.Column(db.Date, nullable=False)
    tanggal_keluar = db.Column(db.Date)
    kamar_id = db.Column(db.Integer, db.ForeignKey('kamar.id', ondelete='SET NULL'))

class Pembayaran(db.Model):
    __tablename__ = 'pembayaran'
    id = db.Column(db.Integer, primary_key=True)
    penghuni_id = db.Column(db.Integer, db.ForeignKey('penghuni.id', ondelete='CASCADE'), nullable=False)
    kamar_id = db.Column(db.Integer, db.ForeignKey('kamar.id', ondelete='CASCADE'), nullable=False)
    bulan = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'lunas'), default='pending')
    metode = db.Column(db.String(50))
    tanggal_bayar = db.Column(db.DateTime)
    bukti_transfer = db.Column(db.String(255))

class Pengaduan(db.Model):
    __tablename__ = 'pengaduan'
    id = db.Column(db.Integer, primary_key=True)
    penghuni_id = db.Column(db.Integer, db.ForeignKey('penghuni.id', ondelete='CASCADE'), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('menunggu', 'diproses', 'selesai'), default='menunggu')
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    tanggapan = db.Column(db.Text)

class Pengumuman(db.Model):
    __tablename__ = 'pengumuman'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    dibuat_oleh = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    pembuat = db.relationship('User', backref='pengumuman_dibuat')

class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    id = db.Column(db.Integer, primary_key=True)
    nama_kegiatan = db.Column(db.String(200), nullable=False)
    tanggal_mulai = db.Column(db.DateTime, nullable=False)
    tanggal_selesai = db.Column(db.DateTime)
    lokasi = db.Column(db.String(200))
    keterangan = db.Column(db.Text)

class Peraturan(db.Model):
    __tablename__ = 'peraturan'
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    dibuat = db.Column(db.DateTime, default=datetime.utcnow)