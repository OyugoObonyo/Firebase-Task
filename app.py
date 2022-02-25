from flask import Flask, redirect, render_template, flash, url_for
import pyrebase
from forms import DownloadForm, UploadForm
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
load_dotenv('.env')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
firebaseConfig = {
  "apiKey": "AIzaSyAgOVNgtr2mWRYRRxupHm0dXI5Pb0BwRjA",
  "authDomain": "file-uploads-e52cd.firebaseapp.com",
  "projectId": "file-uploads-e52cd",
  "storageBucket": "file-uploads-e52cd.appspot.com",
  "messagingSenderId": "59877063629",
  "appId": "1:59877063629:web:e7840f23a8f0f805402284",
  "measurementId": "G-6CRW0DT9V7",
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


@app.route('/')
def index():
    """
    url route for index page
    """
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    route handling file uploads
    """
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        f.filename = secure_filename(f.filename)
        temp = tempfile.NamedTemporaryFile(delete=False)
        f.save(temp.name)
        storage.child(f.filename).put(temp.name)
        # Clean-up temp image
        os.remove(temp.name)
        flash("File was successfully uploaded")
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)


@app.route('/files')
def all_files():
    """
    route that serves up all file names from our firebase storage
    """
    files = storage.child().order_by_child("name").get()
    return render_template('all.html', files=files)



if __name__ == "__main__":
    app.run(debug=True)
