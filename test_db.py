from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/mykost_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        result = db.session.execute(text('SELECT 1'))
        print("✅ Koneksi MySQL berhasil:", result.fetchone())
except Exception as e:
    print("❌ Koneksi gagal:", e)
