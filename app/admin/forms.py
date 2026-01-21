from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField, StringField, TextAreaField, PasswordField, SubmitField, IntegerField, SelectField, DateTimeLocalField, DateField


# =========================
# Form Kelola Penghuni
# =========================
class UnifiedPenghuniForm(FlaskForm):
    # === DATA LOGIN ===
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    
    # === DATA PROFIL ===
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    no_hp = StringField('No. Handphone', validators=[DataRequired()])
    jenis_kelamin = SelectField('Jenis Kelamin', choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], validators=[DataRequired()])
    tanggal_masuk = DateField('Tanggal Masuk', format='%Y-%m-%d', validators=[DataRequired()])
    alamat = TextAreaField('Alamat Asal', validators=[Optional()])

    submit = SubmitField('Simpan Data') 
    

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
class PengaduanForm(FlaskForm):
    pengaduan_id = HiddenField(validators=[DataRequired()])
    tanggapan = TextAreaField('Tanggapan', validators=[DataRequired()])
    submit = SubmitField('Kirim Tanggapan')


# =========================
# Form Tanggapan (Simpan di forms.py atau di atas routes)
# =========================
class TanggapanForm(FlaskForm):
    tanggapan = TextAreaField('Tanggapan', validators=[DataRequired()])
    submit = SubmitField('Kirim')
