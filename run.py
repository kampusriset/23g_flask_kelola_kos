# MyKost Project
# MIT License (c) 2025 AnakKost Team

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)