# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Konfigurasi Database
# Pastikan XAMPP/MySQL sudah Start sebelum menjalankan script ini
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/mykost_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("⏳ Sedang mencoba menghubungkan ke database MySQL...")

try:
    with app.app_context():
        # Test query sederhana (SELECT 1)
        result = db.session.execute(text('SELECT 1'))
        
        print("\n✅ Koneksi MySQL BERHASIL!")
        print(f"   Respon Database: {result.fetchone()}")
        
        # Tambahan: Cek apakah tabel sudah ada
        try:
            tables = db.session.execute(text("SHOW TABLES"))
            list_tabel = [row[0] for row in tables]
            if list_tabel:
                print(f"   Tabel ditemukan ({len(list_tabel)}): {', '.join(list_tabel)}")
            else:
                print("   ⚠️  Koneksi sukses, tapi database masih KOSONG (belum ada tabel).")
        except:
            pass

except Exception as e:
    print("\n❌ Koneksi GAGAL!")
    print(f"   Error: {e}")
    print("\n   Saran:")
    print("   1. Pastikan XAMPP (MySQL) sudah di-Start.")
    print("   2. Pastikan database 'mykost_db' sudah dibuat.")
    print("   3. Cek apakah port 3306 benar digunakan.")