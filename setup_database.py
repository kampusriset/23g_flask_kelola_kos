from pathlib import Path
from urllib.parse import urlparse

import pymysql

from app.config import Config


def _parse_db_uri():
    """Parse URI SQLAlchemy menjadi komponen pymysql."""
    parsed = urlparse(Config.SQLALCHEMY_DATABASE_URI.replace("mysql+pymysql://", "mysql://"))
    return {
        "db_name": parsed.path[1:],
        "user": parsed.username,
        "password": parsed.password or "",
        "host": parsed.hostname,
        "port": parsed.port or 3306,
    }


def create_database(conn_info):
    """Buat database jika belum ada."""
    try:
        connection = pymysql.connect(
            host=conn_info["host"],
            user=conn_info["user"],
            password=conn_info["password"],
            port=conn_info["port"],
            autocommit=True,
            charset="utf8mb4",
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{conn_info['db_name']}` "
                "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
            )
        print(f"[✔] Database `{conn_info['db_name']}` siap!")
    except Exception as exc:
        print(f"[❌] Gagal membuat database: {exc}")
        raise


def apply_sql_dump(conn_info, dump_path: Path):
    """
    Jalankan dump SQL (setup_db.sql) agar struktur & data sama seperti website.
    Hanya baris perintah (abaikan komentar/directive phpMyAdmin).
    """
    if not dump_path.exists():
        print(f"[❌] File dump tidak ditemukan: {dump_path}")
        return

    try:
        raw_sql = dump_path.read_text(encoding="utf-8")
        statements = []
        buffer: list[str] = []

        for line in raw_sql.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("--") or stripped.startswith("/*") or stripped.startswith("/*!"):
                continue

            buffer.append(stripped)
            if stripped.endswith(";"):
                statements.append(" ".join(buffer).rstrip(";"))
                buffer.clear()

        connection = pymysql.connect(
            host=conn_info["host"],
            user=conn_info["user"],
            password=conn_info["password"],
            port=conn_info["port"],
            database=conn_info["db_name"],
            autocommit=True,
            charset="utf8mb4",
        )

        with connection.cursor() as cursor:
            for stmt in statements:
                cursor.execute(stmt)

        connection.close()
        print(f"[✔] Schema & seed dari `{dump_path.name}` berhasil diterapkan.")
    except Exception as exc:
        print(f"[❌] Gagal menerapkan SQL dump: {exc}")
        raise


if __name__ == "__main__":
    print("\n=== 🚀 SETUP DATABASE ===")
    info = _parse_db_uri()
    dump_file = Path(__file__).parent / "setup_db.sql"
    create_database(info)
    apply_sql_dump(info, dump_file)
    print("=== ✔ Selesai ===\n")
