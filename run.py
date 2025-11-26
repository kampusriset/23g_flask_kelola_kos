from app import create_app

# Panggil factory function untuk membuat aplikasi
app = create_app()

if __name__ == "__main__":
    # Jalankan server Flask
    app.run(debug=True)