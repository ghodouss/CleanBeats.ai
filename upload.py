import os
from flask import Flask, request, redirect, url_for, flash,send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename
from audio_cleaner import clean_audio
import requests

#UPLOAD_FOLDER is where we will store the uploaded files
UPLOAD_FOLDER = 'explitive_files'
#allowed format
ALLOWED_EXTENSIONS = set(['mp3','wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']="UPLOAD"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)#use secure_filename function for safety
            filename=file.filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_audio_name = clean_audio(app.config['UPLOAD_FOLDER']+"/"+filename, "em_lyrics.txt")

            
            return redirect(url_for('uploaded_file',
                                    filename=new_audio_name))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload New File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("clean_files/",
                               filename)
# download from the Internet
@app.route('/uploads/test_download_Net/<filename>')
def download_file(url_addr):
    url = url_addr  # user provides url in query string
    r = request.get(url, allow_redirects=True)

    # write to a file in the app's instance folder
    # come up with a better file name
    with app.open_instance_resource('downloaded_file', 'wb') as f:
        f.write(r.content)


@app.route('/uploads/test_download_Local/<filename>')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e)

@app.route('/uploads/return-files/')#the original web use @app.route('/return-files/')
def return_files_tut(filename,address):
    try:
        # example
        # return send_file('/var/www/PythonProgramming/PythonProgramming/static/ohhey.pdf', attachment_filename='ohhey.pdf')
        return send_file(address, attachment_filename=filename)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
