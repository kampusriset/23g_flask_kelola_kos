import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mykost-secret-key'
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:@localhost:3306/mykost_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Maksimal 2 MB
    
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']

    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads/bukti_transfer') 
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Batas ukuran file (opsional, misal 16MB)