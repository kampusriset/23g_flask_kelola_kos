# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Form Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
# Form Register
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar')


# Form Pengaduan
class PengaduanForm(FlaskForm):
    judul = StringField('Judul Pengaduan', validators=[DataRequired(), Length(max=150)])
    isi = TextAreaField('Isi Pengaduan', validators=[DataRequired()])
    submit = SubmitField('Kirim')

# Form Peraturan (admin)
class PeraturanForm(FlaskForm):
    isi = TextAreaField('Isi Peraturan', validators=[DataRequired()])
    submit = SubmitField('Simpan')

# Form Pembayaran (penghuni)
class PembayaranForm(FlaskForm):
    bulan = StringField('Bulan', validators=[DataRequired()])
    jumlah = IntegerField('Jumlah Bayar', validators=[DataRequired()])
    metode = SelectField('Metode Pembayaran', choices=[('transfer', 'Transfer'), ('tunai', 'Tunai')])
    submit = SubmitField('Bayar')
