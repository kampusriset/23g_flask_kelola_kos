# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# --- FORM LOGIN ---
# Digunakan oleh Admin dan Penghuni
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username wajib diisi"),
        Length(min=4, max=100, message="Username minimal 4 karakter")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password wajib diisi")
    ])
    submit = SubmitField('Masuk')

# --- FORM REGISTER ---
# Khusus untuk pendaftaran Admin baru
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username wajib diisi")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password wajib diisi"),
        Length(min=6, message="Password minimal 6 karakter")
    ])
    
    confirm_password = PasswordField('Konfirmasi Password', validators=[
        DataRequired(message="Ulangi password Anda"),
        EqualTo('password', message='Password tidak sama')
    ])
    
    submit = SubmitField('Daftar Admin')