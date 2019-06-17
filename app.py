from flask import Flask, render_template, send_file, url_for, flash, redirect
import process
from os import path
import uuid
from utils.forms import MavenForm
from utils.consts import ABOUT_PUBLIC_MAVEN_XML_EXAMPLE, DOWNLOADED_FILES_DIR, ZIP_EXTENSION
import shutil
import pathlib
app = Flask(__name__)

app.config['SECRET_KEY'] = "ffd4gf78th4ythh49j4s7498dwde4897ry89"


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('public_maven_dependency'),)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='about', public_maven_xml_example=ABOUT_PUBLIC_MAVEN_XML_EXAMPLE)


@app.route('/public_maven_dependency', methods=['GET', 'POST'])
def public_maven_dependency():
    form = MavenForm()
    if form.validate_on_submit():
        # try download the jars
        try:
            jars_zip_path = download_jars(form.maven_xml_pom.data)
            return send_file(jars_zip_path, as_attachment=True, attachment_filename='jars.zip')
        except Exception as e:
            flash('Failed to download the jars', 'danger')
    return render_template('public_maven_dependency.html', title='public maven', form=form)


def download_jars(maven_jar_pom):
    jars_dir_name = str(uuid.uuid4())
    jars_dir_path = str(pathlib.Path(DOWNLOADED_FILES_DIR).joinpath(jars_dir_name))
    process.do_run(maven_jar_pom, jars_dir_path)
    shutil.make_archive(jars_dir_path, ZIP_EXTENSION, jars_dir_path)
    return jars_dir_path + f".{ZIP_EXTENSION}"


if __name__ == '__main__':
    app.run()
