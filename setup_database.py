import pymysql
from urllib.parse import urlparse
from app import app, db
from app.config import Config  # << sesuai struktur kamu


def create_database():
    db_uri = Config.SQLALCHEMY_DATABASE_URI

    parsed = urlparse(db_uri.replace("mysql+pymysql://", "mysql://"))

    db_name = parsed.path[1:]
    user = parsed.username
    password = parsed.password if parsed.password else ""
    host = parsed.hostname
    port = parsed.port or 3306

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4;"
        )
        print(f"[✔] Database `{db_name}` siap!")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"[❌] Gagal membuat database: {e}")


def create_tables():
    try:
        with app.app_context():
            db.create_all()
            print("[✔] Tabel berhasil dibuat dari models!")
    except Exception as e:
        print("[❌] Gagal membuat tabel:", e)


if __name__ == "__main__":
    print("\n=== 🚀 SETUP DATABASE ===")
    create_database()
    create_tables()
    print("=== ✔ Selesai ===\n")
