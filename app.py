from flask import Flask, render_template
import pyrebase
from forms import DownloadForm, UploadForm

app = Flask(__name__)
firebaseConfig = {
  "apiKey": "AIzaSyAgOVNgtr2mWRYRRxupHm0dXI5Pb0BwRjA",
  "authDomain": "file-uploads-e52cd.firebaseapp.com",
  "projectId": "file-uploads-e52cd",
  "storageBucket": "file-uploads-e52cd.appspot.com",
  "messagingSenderId": "59877063629",
  "appId": "1:59877063629:web:e7840f23a8f0f805402284",
  "measurementId": "G-6CRW0DT9V7"
}
# initialize pyrebase app
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


@app.route('/')
def index():
    """
    url route for index page
    """
    return render_template('index.html')


@app.route('/upload')
def upload_file():
    """
    route handling file uploads
    """
    form = UploadForm()
    return render_template('upload.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
