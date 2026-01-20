from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# USER (LOGIN)
# =========================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum('admin', 'penghuni'),
        default='penghuni',
        nullable=False
    )

    # NULL = belum upload foto
    profile_photo = db.Column(db.String(255), nullable=True)
    bg_profile_photo = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.username}>"



# =========================
# KAMAR
# =========================
class Kamar(db.Model):
    __tablename__ = 'kamar'

    id = db.Column(db.Integer, primary_key=True)
    nomor_kamar = db.Column(db.String(50), unique=True, nullable=False)
    tipe = db.Column(db.String(50))
    harga = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum('kosong', 'terisi'),
        default='kosong'
    )
    fasilitas = db.Column(db.Text)
    keterangan = db.Column(db.Text)

    def __repr__(self):
        return f"<Kamar {self.nomor_kamar}>"

# =========================
# PENGHUNI
# =========================
class Penghuni(db.Model):
    __tablename__ = 'penghuni'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    nama = db.Column(db.String(150), nullable=False)
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    jenis_kelamin = db.Column(db.Enum('L', 'P'))
    tanggal_masuk = db.Column(db.Date, nullable=False)
    tanggal_keluar = db.Column(db.Date)

    kamar_id = db.Column(
        db.Integer,
        db.ForeignKey('kamar.id', ondelete='SET NULL')
    )

    user = db.relationship(
        'User',
        backref=db.backref('penghuni', uselist=False)
    )

    kamar = db.relationship(
        'Kamar',
        backref=db.backref('penghuni', lazy=True)
    )

    def __repr__(self):
        return f"<Penghuni {self.nama}>"

# =========================
# PENGADUAN
# =========================
class Pengaduan(db.Model):
    __tablename__ = 'pengaduan'

    id = db.Column(db.Integer, primary_key=True)

    penghuni_id = db.Column(
        db.Integer,
        db.ForeignKey('penghuni.id', ondelete='CASCADE'),
        nullable=False
    )

    judul = db.Column(db.String(150), nullable=False)
    isi = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.Enum('menunggu', 'diproses', 'selesai', name='status_pengaduan'),
        default='menunggu',
        nullable=False
    )

    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    tanggapan = db.Column(db.Text)

    penghuni = db.relationship(
        'Penghuni',
        backref=db.backref(
            'pengaduan',
            lazy=True,
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f"<Pengaduan {self.judul}>"

# =========================
# PENGUMUMAN
# =========================
class Pengumuman(db.Model):
    __tablename__ = 'pengumuman'

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    dibuat_oleh = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    pembuat = db.relationship(
        'User',
        backref=db.backref('pengumuman', lazy=True)
    )

    def __repr__(self):
        return f"<Pengumuman {self.judul}>"

# =========================
# PERATURAN
# =========================
class Peraturan(db.Model):
    __tablename__ = 'peraturan'

    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    dibuat = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Peraturan {self.id}>"

# =========================
# JADWAL
# =========================
class Jadwal(db.Model):
    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True)
    nama_kegiatan = db.Column(db.String(200), nullable=False)
    tanggal_mulai = db.Column(db.DateTime, nullable=False)
    lokasi = db.Column(db.String(200))
    keterangan = db.Column(db.Text)

    def __repr__(self):
        return f"<Jadwal {self.nama_kegiatan}>"
    

# =========================
# PEMBAYARAN
# =========================
class Pembayaran(db.Model):
    __tablename__ = 'pembayaran'

    id = db.Column(db.Integer, primary_key=True)
    penghuni_id = db.Column(db.Integer, nullable=False)
    kamar_id = db.Column(db.Integer, nullable=False)
    bulan = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'lunas', name='status_enum'), default='pending')
    metode = db.Column(db.String(50), nullable=True)
    tanggal_bayar = db.Column(db.DateTime, nullable=True, default=None)
    bukti_transfer = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Pembayaran {self.id} - {self.status} - {self.jumlah}>"