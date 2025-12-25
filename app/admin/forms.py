from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
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
