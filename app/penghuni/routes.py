from datetime import datetime
from flask import render_template
from flask_login import login_required, current_user

from app.models import Pengumuman, Peraturan, Jadwal
from app.utils.decorators import role_required


from . import penghuni_bp


@penghuni_bp.route('/dashboard')
@login_required
@role_required('penghuni')
def dashboard():
    return render_template(
        'dashboard_penghuni.html',
        sidebar='partials/sidebar_penghuni.html'
    )




@penghuni_bp.route('/pengumuman')
@login_required
@role_required('penghuni')
def pengumuman():
    semua_pengumuman = Pengumuman.query.order_by(
        Pengumuman.tanggal.desc()
    ).all()

    return render_template(
        'pengumuman_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        semua_pengumuman=semua_pengumuman
    )




@penghuni_bp.route('/peraturan')
@login_required
@role_required('penghuni')
def peraturan():
    semua_peraturan = Peraturan.query.all()

    return render_template(
        'peraturan_penghuni.html',
        sidebar='partials/sidebar_penghuni.html',
        semua_peraturan=semua_peraturan
    )

@penghuni_bp.route('/jadwal')
@login_required
@role_required('penghuni')
def jadwal():
    # Menampilkan jadwal dari yang terdekat
    semua_jadwal = Jadwal.query.filter(Jadwal.tanggal_mulai >= datetime.utcnow()).order_by(Jadwal.tanggal_mulai.asc()).all()
    return render_template('jadwal_penghuni.html', sidebar='partials/sidebar_penghuni.html', semua_jadwal=semua_jadwal)