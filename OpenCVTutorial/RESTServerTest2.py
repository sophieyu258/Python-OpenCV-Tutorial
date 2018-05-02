import os
import cv2
import numpy as np

from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '..\\data\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def flash(message):
    print(message)

def get_np_array_from_filestorage(fstore):
     '''converts a buffer from a FileStorage in np.array'''
     ba = bytearray(fstore.read())
     return np.asarray(ba, dtype=np.uint8)

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
        if 'firstname' in request.form:
            print(request.form['firstname'])
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            savedFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(savedFile)
            img = cv2.imread(savedFile)
            #img = cv2.imread(get_np_array_from_filestorage(file))
            #print(img)
            if not img is None:    
                #small = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
                small = cv2.resize(img, (640,480))            
                cv2.imshow('halfsize',small)
                cv2.waitKey(1)
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <input type="text" name="firstname" value="Mickey">
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=888)
