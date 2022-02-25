from flask import Flask, redirect, render_template, flash, url_for
import pyrebase
from forms import UploadForm
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
  "databaseURL": "",
  "serviceAccount": "file-uploads-e52cd-firebase-adminsdk-43rlq-c5138d85db.json"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


@app.route('/')
def index():
    """
    url route for index page
    """
    files = storage.list_files()
    # get names of all files available in storage 
    file_names = [(storage.child(file.name).get_url(None))[77:-10] for file in files]
    return render_template('index.html', file_names=file_names)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    route handling file uploads
    """
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        # Ensure filename doesn't have inappropriate characters such as /
        f.filename = secure_filename(f.filename)
        # Save file temporarily in our file system
        temp = tempfile.NamedTemporaryFile(delete=False)
        f.save(temp.name)
        storage.child(f.filename).put(temp.name)
        # Clean-up temp file
        os.remove(temp.name)
        flash("File was successfully uploaded", "success")
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)


@app.route('/download/<filename>')
def download_file(filename):
    """
    download_file: downloads a file from firebase storage
    @filename -Name of file we want to download
    """
    url = storage.child(filename).get_url(None)
    return redirect(url)


if __name__ == "__main__":
    app.run()
