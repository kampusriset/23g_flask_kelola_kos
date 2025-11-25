import os

class Config:
    # Kunci rahasia untuk sesi dan keamanan form
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey123'
    
    # Konfigurasi Database MySQL
    # Pastikan formatnya: mysql+pymysql://username:password@host:port/nama_db
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/mykost_db'
    
    # Mematikan notifikasi perubahan objek (menghemat memori)
    SQLALCHEMY_TRACK_MODIFICATIONS = False