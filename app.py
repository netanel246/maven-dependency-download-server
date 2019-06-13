from flask import Flask
import process

app = Flask(__name__)


@app.route('/copy_only_new_files', methods=['GET'])
def copy_only_new_files(pom):
    argv = [pom]
    process.do_run(argv)


if __name__ == '__main__':
    app.run()
