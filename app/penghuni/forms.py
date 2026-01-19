from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, TextAreaField, PasswordField, SubmitField
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
class PembayaranForm(FlaskForm):
    # Data Tagihan
    kamar_id = IntegerField('ID Kamar', validators=[DataRequired(message="ID Kamar harus diisi")])
    bulan = StringField('Bulan Tagihan', validators=[DataRequired(message="Bulan harus diisi (cth: Januari 2026)")])
    jumlah = IntegerField('Jumlah (Rp)', validators=[DataRequired(message="Nominal harus diisi")])

    # Metode Pembayaran
    metode = SelectField(
        'Metode Pembayaran',
        choices=[
            ('Cash', 'Tunai (Cash)'),
            ('Transfer BCA', 'Transfer BCA - 1234567890'),
            ('Transfer Mandiri', 'Transfer Mandiri - 0987654321'),
            ('Transfer BNI', 'Transfer BNI - 1122334455')
        ],
        validators=[DataRequired()]
    )

    # Bukti Transfer
    bukti_transfer = FileField('Bukti Transfer', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya file gambar yang diperbolehkan!'),
        Optional()
    ])

    submit = SubmitField('Konfirmasi Pembayaran')