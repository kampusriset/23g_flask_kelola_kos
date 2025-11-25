from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

@app.cli.command("create-admin")
def create_admin():
    db.create_all()
    # Cek apakah admin sudah ada
    if not User.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        # Sesuaikan dengan model User yang baru (tanpa nama_lengkap di tabel users)
        admin = User(username='admin', password=hashed_pw, role='admin', email='admin@mykost.com')
        db.session.add(admin)
        db.session.commit()
        print("User admin berhasil dibuat!")
    else:
        print("Admin sudah ada.")

if __name__ == '__main__':
    app.run(debug=True)