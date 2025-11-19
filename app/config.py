# MyKost Project
# MIT License (c) 2025 AnakKost Team

import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey123'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/mykost_db'

SQLALCHEMY_TRACK_MODIFICATIONS = False