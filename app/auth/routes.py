from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.models import Pengaduan
from app.forms import PengaduanForm
from datetime import datetime

@app.route('/pengaduan')
@login_required
def list_pengaduan():
    pengaduan_list = Pengaduan.query.filter_by(penghuni_id=current_user.id).all()
    return render_template('aduan.html', pengaduan_list=pengaduan_list)

@app.route('/pengaduan/tambah', methods=['GET', 'POST'])
@login_required
def tambah_pengaduan():
    form = PengaduanForm()
    if form.validate_on_submit():
        aduan = Pengaduan(
            penghuni_id=current_user.id,
            judul=form.judul.data,
            isi=form.isi.data,
            tanggal=datetime.utcnow()
        )
        db.session.add(aduan)
        db.session.commit()
        flash('Pengaduan berhasil dikirim')
        return redirect(url_for('list_pengaduan'))
    return render_template('form_pengaduan.html', form=form)

@app.route('/pengaduan/hapus/<int:id>')
@login_required
def hapus_pengaduan(id):
    aduan = Pengaduan.query.get_or_404(id)
    if aduan.penghuni_id != current_user.id:
        flash('Akses ditolak')
        return redirect(url_for('list_pengaduan'))
    db.session.delete(aduan)
    db.session.commit()
    flash('Pengaduan berhasil dihapus')
    return redirect(url_for('list_pengaduan'))