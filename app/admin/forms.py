from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, SelectField, DateTimeLocalField


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


# =========================
# Form Jadwal
# =========================
class JadwalForm(FlaskForm):
    nama_kegiatan = StringField('Nama Kegiatan', validators=[DataRequired()])
    tanggal_mulai = DateTimeLocalField('Waktu Mulai', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    lokasi = StringField('Lokasi (Opsional)')
    keterangan = TextAreaField('Detail Kegiatan')
    submit = SubmitField('Simpan Jadwal')


# =========================  
# Form Pengaduan
# =========================
class TanggapanForm(FlaskForm):
    tanggapan = TextAreaField('Berikan Tanggapan', validators=[DataRequired()])
    submit = SubmitField('Kirim Tanggapan')
