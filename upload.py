import os
from flask import *
from audio_cleaner import clean_audio

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


if __name__ == "__main__":
    app.run(debug=True)