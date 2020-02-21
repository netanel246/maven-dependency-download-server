from flask import Flask, render_template, send_file, url_for, flash, redirect, after_this_request
from flask_cors import CORS
import process
import uuid
from utils.forms import MavenForm
from utils.consts import ABOUT_PUBLIC_MAVEN_XML_EXAMPLE, DOWNLOADED_FILES_DIR, ZIP_EXTENSION
import shutil
import pathlib
import tempfile


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "ffd4gf78th4ythh49j4s7498dwde4897ry89"


# prevent cached responses

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


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
        working_dir = tempfile.TemporaryDirectory()

        @after_this_request
        def clean_directory(response):
            working_dir.cleanup()
            return response

        try:
            jars_zip_path = download_jars(form.maven_xml_pom.data, working_dir.name)
            # return send_file(jars_zip_path, as_attachment=True, attachment_filename='jars.zip')

            in_file = open(jars_zip_path, "rb")
            data = in_file.read()
            in_file.close()

            return_value = app.response_class(data)
            return_value.headers.set('Content-Disposition', 'attachment', filename='jars.zip')
            return_value.headers.set('Content-Type', 'application/x-zip-compressed')
            return return_value
        except Exception as e:
            print(e)
            flash('Failed to download the jars: {}'.format(e), 'danger')
    return render_template('public_maven_dependency.html', title='public maven', form=form)


def download_jars(maven_jar_pom, jars_dir_temp_base):
    jars_dir_name = DOWNLOADED_FILES_DIR  # str(uuid.uuid4())
    jars_dir_path = str(pathlib.Path(jars_dir_temp_base).joinpath(jars_dir_name))

    process.do_run(maven_jar_pom, jars_dir_path)
    shutil.make_archive(jars_dir_path, ZIP_EXTENSION, jars_dir_path)
    return jars_dir_path + ".{}".format(ZIP_EXTENSION)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
