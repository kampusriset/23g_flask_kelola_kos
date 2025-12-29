from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PengaduanForm(FlaskForm):
    judul = StringField('Judul Pengaduan', validators=[DataRequired()])
    isi = TextAreaField('Detail Masalah', validators=[DataRequired()])
    submit = SubmitField('Kirim Laporan')