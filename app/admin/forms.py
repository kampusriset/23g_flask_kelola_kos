from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email

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
# Form Kamar (Admin)
# =========================
class KamarForm(FlaskForm):
    nomor_kamar = StringField('Nomor Kamar', validators=[DataRequired()])
    tipe = StringField('Tipe Kamar', validators=[DataRequired()])
    harga = IntegerField('Harga (Rp)', validators=[DataRequired()])
    status = SelectField('Status', choices=[('kosong', 'Kosong'), ('terisi', 'Terisi')], default='kosong')
    fasilitas = TextAreaField('Fasilitas')
    keterangan = TextAreaField('Keterangan Tambahan')
    penghuni_id = SelectField('Penghuni (Opsional)', coerce=int, choices=[], default=0)
    submit = SubmitField('Simpan Kamar')