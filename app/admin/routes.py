from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Decorator khusus Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/kamar')
@login_required
@admin_required
def kamar():
    # Logika ambil data kamar dari DB
    return render_template('admin/kamar.html')