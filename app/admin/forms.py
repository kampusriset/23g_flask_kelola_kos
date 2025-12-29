from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import DateTimeLocalField

# =========================
# Form Buat Penghuni
# =========================
class PenghuniForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Simpan')


# =========================
# Form Peraturan
# =========================
class PeraturanForm(FlaskForm):
    isi = TextAreaField('Isi Peraturan', validators=[DataRequired()])
    submit = SubmitField('Tambah Peraturan')


# =========================
# Form Pengumuman
# =========================
class PengumumanForm(FlaskForm):
    judul = StringField('Judul Pengumuman', validators=[DataRequired()])
    isi = TextAreaField('Isi Pengumuman', validators=[DataRequired()])
    submit = SubmitField('Tambah Pengumuman')

# =========================
# Form Jadwal
# =========================
class JadwalForm(FlaskForm):
    nama_kegiatan = StringField('Nama Kegiatan', validators=[DataRequired()])
    tanggal_mulai = DateTimeLocalField('Waktu Mulai', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    lokasi = StringField('Lokasi (Opsional)')
    keterangan = TextAreaField('Detail Kegiatan')
    submit = SubmitField('Simpan Jadwal')
# Form Pengaduan
# =========================
# Tambahkan di app/admin/forms.py
class TanggapanForm(FlaskForm):
    tanggapan = TextAreaField('Berikan Tanggapan', validators=[DataRequired()])
    submit = SubmitField('Kirim Tanggapan')
