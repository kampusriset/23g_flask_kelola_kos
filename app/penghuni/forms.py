from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PengaduanForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired(), Length(max=150)])
    kamar = StringField('Kamar', validators=[DataRequired(), Length(max=50)])
    laporan = TextAreaField('Laporan', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Kirim Laporan')
