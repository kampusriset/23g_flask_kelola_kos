# 23g_flask_kelola_kos_MyKost
# MyKost App

MyKost adalah aplikasi manajemen kos berbasis Flask, MySQL/MariaDB, dan TailwindCSS.
Aplikasi ini digunakan untuk mengelola data kamar, penghuni, pembayaran, pengaduan,
dan pengumuman kos dengan sistem role Admin dan Penghuni.

----------------------------------------------------------------

TECH STACK
- Backend  : Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login
- Database : MySQL / MariaDB
- Frontend : TailwindCSS
- ORM      : SQLAlchemy
- Auth     : Session-based authentication

----------------------------------------------------------------

CARA MENJALANKAN PROYEK

1. FRONTEND (TailwindCSS)
Pastikan Node.js sudah terinstall.

Perintah:
npm install
npm run dev

----------------------------------------------------------------

2. BACKEND (Flask)

Buat virtual environment dan install dependency:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

----------------------------------------------------------------

KONFIGURASI APLIKASI

Edit file app/config.py:

class Config:
    SECRET_KEY = 'mykost-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/mykost_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

Pastikan database mykost_db sudah dibuat di MySQL/MariaDB.

----------------------------------------------------------------

SETUP DATABASE

Project ini menggunakan Flask-Migrate untuk mengelola perubahan struktur database.

DATABASE BARU (KOSONG)

DATABASE BARU (KOSONG)

1. Buat database kosong di MySQL / MariaDB:

   mykost_db

2. Jalankan migrasi database:

   flask db upgrade

Perintah ini akan membuat seluruh tabel berdasarkan
migration yang sudah tersedia di project.

----------------------------------------------------------------
MEMBUAT DATA AWAL (SEED)

Untuk membuat user default (admin & penghuni), jalankan:

   python seed.py

User default:
- Admin     : admin / admin123
- Penghuni  : penghuni1 / user123

⚠️ Disclaimer:
Segera ubah username dan password default
demi keamanan aplikasi.

----------------------------------------------------------------

WORKFLOW PERUBAHAN DATABASE

Setiap ada perubahan model:

flask db migrate -m "deskripsi perubahan"
flask db upgrade

Rollback jika diperlukan:

flask db downgrade

----------------------------------------------------------------

MENJALANKAN APLIKASI

flask run

Akses aplikasi melalui browser:
http://127.0.0.1:5000

----------------------------------------------------------------

STRUKTUR FOLDER (RINGKAS)

MyKost/
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── config.py
├── migrations/
│   └── versions/
├── sql/
│   └── setup_db.sql
├── setup_database.py
├── requirements.txt
├── README.md
└── .gitignore

----------------------------------------------------------------

CATATAN PENTING

- Folder berikut TIDAK BOLEH di-commit ke GitHub:
  venv/
  .env
  __pycache__/
  database lokal

- File setup_db.sql hanya digunakan untuk setup awal database kosong
- Semua perubahan schema database HARUS lewat Flask-Migrate
- Jangan menjalankan setup_database.py di production

----------------------------------------------------------------

ROLE PENGGUNA

ADMIN:
- Mengelola kamar
- Mengelola penghuni
- Mengelola pengumuman
- Melihat dan memvalidasi pembayaran

PENGHUNI:
- Melihat data kamar
- Melakukan pembayaran
- Mengirim pengaduan
- Melihat pengumuman

----------------------------------------------------------------

STATUS PROYEK

Dalam pengembangan

Fitur utama:
- Manajemen kamar
- Manajemen penghuni
- Pembayaran kos
- Pengaduan
- Pengumuman
- Sistem login dan role

----------------------------------------------------------------

LISENSI

Project ini dibuat untuk keperluan pembelajaran dan pengembangan internal.

Aplikasi siap digunakan.
