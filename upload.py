import os
from flask import *

#UPLOAD_FOLDER is where we will store the uploaded files
UPLOAD_FOLDER = '/Users/yuyang/Desktop/temp'
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
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!DOCTYPE html>
<html>
	<head>
        <title>Clean Beats</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    		<link rel="stylesheet" href="style.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    </head>
	<body>
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="https://github.com/ghodouss/CleanBeats.ai" target="_blank">CleanBeats.ai</a>
        </div>

      </div>
    </nav>
    <div class="bodyContainer">
      <header>
        <h1 id="headerTitle">CLEAN BEATS</h1>
      </header>
      <div>
        Make non-explicit versions of your songs to play at your holiday party!
      </div>
      <br />
      <div id="formContainer">
      <form action="/uploadsong" method="post" enctype=multipart/form-data>
        <input name="songFile" type="file">
        <br />
        <input type="submit" value="upload">
      </form>
      </div>
    </div>
	</body>
</html>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run()
