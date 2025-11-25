from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort

penghuni_bp = Blueprint('penghuni', __name__, template_folder='templates')

# Decorator khusus Penghuni
def penghuni_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'penghuni':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@penghuni_bp.route('/dashboard')
@login_required
@penghuni_required
def index():
    return render_template('penghuni/index.html')

@penghuni_bp.route('/pengaduan')
@login_required
@penghuni_required
def pengaduan():
    return render_template('penghuni/pengaduan.html')