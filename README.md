<img width="746" height="1091" alt="image" src="https://github.com/user-attachments/assets/d6995491-4acb-4205-9941-119d7473dc95" /># 23g_flask_kelola_kos_MyKost
# MyKost

MyKost adalah aplikasi manajemen kos berbasis Flask, MySQL/MariaDB, dan TailwindCSS.
Aplikasi ini digunakan untuk mengelola data kamar, penghuni, pembayaran, pengaduan,
dan pengumuman kos dengan sistem role Admin dan Penghuni.

----------------------------------------------------------------
# Team
- **Nafan Baihaqi** - [2313010563]
- **Bagas Putra Baharuddin** - [2313010571]
- **Muhammad Daffa Dzaki P** - [2313010546]
- **Rafi Alif Firdaus** - [2313010560]

----------------------------------------------------------------
# Link Video Dokumentasi
Anda dapat menonton video dokumentasi aplikasi melalui tautan berikut:
[Klik di sini](https://youtu.be/NyZH2sPjc00)

----------------------------------------------------------------
# Flowchart
<img width="746" height="1091" alt="image" src="https://github.com/user-attachments/assets/d6995491-4acb-4205-9941-119d7473dc95" />

----------------------------------------------------------------

STRUKTUR FOLDER (RINGKAS)

    MyKost/
    ├── app/
    │   ├── admin/
    │   ├── auth/
    │   ├── penghuni/
    │   ├── seeds/
    │   ├── static/
    │   ├── templates/
    │   ├── utils/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── extensions.py
    │   └── models.py
    ├── migrations/
    ├── Teams/
    ├── .gitignore
    ├── LICENSE
    ├── package.json
    ├── package-lock.json
    ├── README.md
    ├── requirements.txt
    ├── run.py
    ├── seed.py
    ├── tailwind.config.js
    └── test_db.py


----------------------------------------------------------------

CATATAN PENTING

- Folder berikut TIDAK BOLEH di-commit ke GitHub:
  venv/
  .env
  node_modules/
  __pycache__/
  database lokal

- Semua perubahan schema database HARUS lewat Flask-Migrate

----------------------------------------------------------------

ROLE PENGGUNA

ADMIN:
- Mengelola kamar
- Mengelola penghuni
- Mengelola pengumuman
- Mengelola peraturan
- Mengelola jadwal
- Melihat dan memvalidasi pembayaran
- Melihat profil
- Melihat pengaduan

PENGHUNI:
- Melihat data kamar
- Melakukan pembayaran
- Mengirim pengaduan
- Melihat pengumuman
- Melihat jadwal
- Melihat peraturan
- Melihat profil

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
LISENSI

MIT License

