import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def save_image(file, folder, old_file=None):
    """
    file       : FileStorage
    folder     : 'uploads/profile' / 'uploads/bg_profile'
    old_file   : path lama di DB
    """

    # jika tidak upload file baru
    if not file or not hasattr(file, 'filename') or file.filename == '':
        return old_file

    # ambil ekstensi
    ext = os.path.splitext(file.filename)[1].lower()

    # validasi ekstensi
    allowed_ext = current_app.config.get('UPLOAD_EXTENSIONS', [])
    if ext not in allowed_ext:
        raise ValueError('Format file tidak diizinkan')

    # generate nama uuid
    filename = f"{uuid.uuid4().hex}{ext}"

    upload_dir = os.path.join(current_app.static_folder, folder)
    os.makedirs(upload_dir, exist_ok=True)

    new_path = os.path.join(upload_dir, filename)
    file.save(new_path)

    # hapus file lama (kecuali default)
    if old_file and old_file.startswith('uploads/'):
        old_path = os.path.join(current_app.static_folder, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)

    return f"{folder}/{filename}"
