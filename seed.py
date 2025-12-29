from app import create_app
from app.seeds.users import seed_users

app = create_app()

with app.app_context():
    seed_users()