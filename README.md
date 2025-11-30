# 23g_flask_kelola_kos_MyKost
# MyKost App

Aplikasi manajemen kos berbasis Flask, MySQL, dan TailwindCSS.

## Cara Menjalankan Proyek

1. Install dan jalankan Tailwind:
   npm install
   npm run dev

2. Install dan jalankan Backend (Flask):
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Setup Database secara otomatis:
   python setup_database.py

4. Jalankan Aplikasi:
   flask run

5. Akses aplikasi melalui:
   http://127.0.0.1:5000

## Konfigurasi (File: app/config.py)

class Config:
    SECRET_KEY = 'mykost-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/mykost_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

Aplikasi siap digunakan 🚀
