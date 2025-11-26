from flask import render_template
from flask_login import login_required
from . import penghuni_bp

@penghuni_bp.route('/')
@login_required
def index():
    return render_template('index.html')