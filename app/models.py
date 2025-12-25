from app import db
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

class Peraturan(db.Model):
    __tablename__ = 'peraturan'
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)

class Pengumuman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=db.func.current_timestamp())
    dibuat_oleh = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relasi ke User (opsional, biar bisa akses nama pembuat)
    pembuat = db.relationship('User', backref='pengumuman')


