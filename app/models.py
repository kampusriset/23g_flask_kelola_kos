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

class Kamar(db.Model):
    __tablename__ = 'kamar'
    id = db.Column(db.Integer, primary_key=True)
    nomor_kamar = db.Column(db.String(50), unique=True, nullable=False)
    tipe = db.Column(db.String(50))
    harga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('kosong', 'terisi'), default='kosong')
    fasilitas = db.Column(db.Text)
    keterangan = db.Column(db.Text)