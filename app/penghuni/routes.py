from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import penghuni_bp
from app import db
from app.models import Pengaduan
from .forms import PengaduanForm


@penghuni_bp.route('/')
@login_required
def index():
    return render_template('index.html')


@penghuni_bp.route('/pengaduan', methods=['GET', 'POST'])
@login_required
def pengaduan():
    form = PengaduanForm()
    if form.validate_on_submit():
        p = Pengaduan(
            nama=form.nama.data,
            kamar=form.kamar.data,
            laporan=form.laporan.data,
            user_id=getattr(current_user, 'id', None)
        )
        db.session.add(p)
        try:
            db.session.commit()
            flash('Laporan pengaduan berhasil dikirim.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menyimpan pengaduan: {e}', 'danger')
        return redirect(url_for('penghuni.pengaduan'))

    return render_template('pengaduan.html', form=form)