from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileField, FileAllowed


# =========================
# Form Pengaduan
# =========================
class PengaduanForm(FlaskForm):
    judul = StringField('Judul Pengaduan', validators=[DataRequired()])
    isi = TextAreaField('Detail Masalah', validators=[DataRequired()])
    submit = SubmitField('Kirim Laporan')


# =========================
# Form Profile
# =========================
class ProfileForm(FlaskForm):
    profile_photo = FileField('Foto Profil',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Hanya file gambar yang diperbolehkan!')
        ]
    )
    bg_profile_photo = FileField(
        'Foto Latar Profil',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Hanya file gambar yang diperbolehkan!')
        ]
    )
    username = StringField('Username', validators=[DataRequired(message='Username wajib diisi')])
    email = StringField('Email', validators=[Optional(), Email(message='Format email tidak valid')])
    password = PasswordField('Password', validators=[Optional()])
    submit = SubmitField('Update Profile')

    # =========================  
# Form Pengaduan
# =========================
class TanggapanForm(FlaskForm):
    tanggapan = TextAreaField('Berikan Tanggapan', validators=[DataRequired()])
    submit = SubmitField('Kirim Tanggapan')

    # =========================
    # Form Pembayaran
    # =========================
    class PaymentForm(FlaskForm):
        metode = SelectField(
            'Metode Pembayaran',
            choices=[('cash', 'Cash'), ('transfer', 'Transfer')],
            validators=[DataRequired()]
        )
        bank = StringField('Bank (Opsional)', validators=[Optional()])
        submit = SubmitField('Konfirmasi Pembayaran')