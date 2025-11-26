import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mykost-secret-key'
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:@localhost:3306/mykost_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False