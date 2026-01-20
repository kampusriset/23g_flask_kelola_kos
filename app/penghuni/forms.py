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
# Form Pembayaran (REVISI)
# =========================
class PembayaranForm(FlaskForm):
    # 1. Hapus 'kamar_id'. Kita tidak butuh input ini dari user karena
    #    kita ambil ID-nya otomatis di routes.py berdasarkan user yang login.
    
    # 2. Field Nomor Kamar (Cukup satu saja)
    # render_kw={'readonly': True} membuat field ini tidak bisa diedit di HTML
    nomor_kamar = StringField('Nomor Kamar', render_kw={'readonly': True})
    
    # 3. Bulan & Jumlah
    # Walaupun di HTML readonly, tetap perlu ada di sini agar bisa dirender
    bulan = StringField('Bulan Tagihan', validators=[DataRequired()])
    jumlah = IntegerField('Jumlah (Rp)', validators=[DataRequired()])

    # 4. Metode Pembayaran
    metode = SelectField(
        'Metode Pembayaran',
        choices=[
            ('Transfer', 'Transfer Bank'), # Saya sederhanakan value-nya biar mudah dicek di if 'Transfer'
            ('Cash', 'Tunai (Cash)')
        ],
        validators=[DataRequired()]
    )

    # 5. Bukti Transfer
    # Pakai Optional() karena kalau bayar Tunai, file ini tidak wajib.
    # Validasi wajib-nya sudah kita tangani manual di routes.py
    bukti_transfer = FileField('Bukti Transfer', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya file gambar (JPG/PNG)!'),
        Optional()
    ])

    submit = SubmitField('Konfirmasi Pembayaran')