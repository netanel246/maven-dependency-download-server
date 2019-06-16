from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MavenForm(FlaskForm):
    maven_xml_pom = TextAreaField('maven xml pom', validators=[DataRequired()])
    submit_download_jars = SubmitField('Download jars')