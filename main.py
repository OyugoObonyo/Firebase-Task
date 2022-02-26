from flask import Flask, redirect, render_template, flash, url_for
import pyrebase
from forms import UploadForm
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import tempfile


app = Flask(__name__)
load_dotenv('.env')

firebaseConfig = {
  "apiKey": "AIzaSyAgOVNgtr2mWRYRRxupHm0dXI5Pb0BwRjA",
  "authDomain": "file-uploads-e52cd.firebaseapp.com",
  "projectId": "file-uploads-e52cd",
  "storageBucket": "file-uploads-e52cd.appspot.com",
  "messagingSenderId": "59877063629",
  "appId": "1:59877063629:web:e7840f23a8f0f805402284",
  "measurementId": "G-6CRW0DT9V7",
  "databaseURL": "",
  "serviceAccount": {
        "type": "service_account",
        "project_id": "file-uploads-e52cd",
        "private_key_id": "0abedd31197b9fb5abcb93df0772824ee42b7828",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDBc9+6roqIQd7l\npPoFxHnTUHDjtClpVu9i5/C+Bik/tJ2XGguEbmNI4DlPmELV6Tx/3vuW5OKh6Dv1\nHeVNlH/5o11t8tA2REBDDL46mnWmpq7kFxfMxLwbzGJ9o+avgWChS72WFcLf6YgQ\nw5EUbt6PLbdqjfcPdxNQEGWp3HrtH5o1BzDjKIO8C4ed0ya7IeOTInxfS0/ZNQYt\nY0U9HJ7TGRka5M0aswDGCkeEWFoHqjao8aiBGZ+KkRPx41DFq/2etE4eV85iYDAy\n7+EX4WQF6EpuV4eAeEqhSOWrlKe9dsRdlu5IwwLa8JzBrfwqPetTOBM7OeaXAYll\nVPibL0h7AgMBAAECggEAB6FjbMCftDos6Y/1UK7sQzqECWc8zuvf613MsCIcFGgy\nYxhi5elYvzIg8JPH5xoZCc4ozE3g5pP7cXKpbcLyvU0FTWXrcoiEpGBnTHZ1N4qR\nkWubw7bq2InaRKxnV/rZbeNH6hiXpC9Y75hXK6An5SvfdTN+UDzZJSpQaD/LFXk8\n6b8HapZw3sRuJZPuefs3OqQ9cA+MIbWXRMomNGdhk9ILPhvvTygeZNmKxoaiWLvu\nho8JNuIwo/b14rBVEe8eRP2oConesZ0GaQTCgOuzp5RJshEuWIHqM7rye7/kIib+\n+yXFF+B12728O8Bzvriz/RyBNukPxBSJpSuV20ltCQKBgQD/ezcoDvmHtHtqvnzc\njJEFMdFrv6WET2OZPq6TVrwKVrzqb6cJHceH50gRwUF5VFNwYdQLlIidWjEUcMrN\nW7+hWnYAZT4hPVuhJnCppHM2NL6wzgh65BHg6jAxvvLVgnLSwVnZQMm7tl6iqFEl\nQO1gSdzbW002Qvp8xTtDj5Ma5wKBgQDB2GtmpqR9vfOmOu9KSiCkwdPHzf8aiont\nCxY+LLtLxpK+QF4CRUU9jXV/I4G/MOKVTpYokYPiYlO7mjqBaB8+P7H4iRQCKn4R\n3e9FJioWHs9amyvaCTYdGVKEUc5/IzwVDMO+NtxJmUVtUzqfu5236rTPjU3F50Jl\nr1QiSpEnTQKBgQDygwHOcriHCtmEcCGSMZSPe8SxJRB20e1XUFri3ZhNsBxP5YCH\ndM8swGx2/h2qkFNMAHEKNQqhYzXnk1HPMeJrxbTxlyks4FOUWyrivYnn0JWau1jt\nXoViHKt27S0RY2yfho5FXeyg1PJsMJ4mYMVze2m8h6R5d4bS3V3uOeGHzQKBgQCB\no/HARza/eahXxhZ/ArBuP8sZV6WC5KB1zfJkRppEhVtirb2xmw5BqjeofeCqM1F2\nNYarPxaK8uO5Fd6G6VHr2cF2zIZ7JFwIKvt4rZt8C8L1f82GFp8AOw06vVNzJ+do\n1I6cyiftePo7sWwFo/5JIEkofgJDlvSK+QU1odUOCQKBgQCnUeF7ocmhv5sHNJqn\n0kOA15VAmyTMPwH25nfaDKaePMZmZyBxcXmrtq4TD6lsZJZfjbn7qlZkf94wfQcC\nUsBFL7UNMelbPgSBlbHSVGj1WIbc7opOq2X6VgTHEkLEA0noGBOIO9N13v3dgWbC\n9fIBz7eyc1Wj+0jIzh29nVDBcw==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-43rlq@file-uploads-e52cd.iam.gserviceaccount.com",
        "client_id": "117133973667958498239",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-43rlq%40file-uploads-e52cd.iam.gserviceaccount.com"
    }
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
    app.run(debug=True)
