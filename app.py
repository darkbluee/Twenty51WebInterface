import os
import sqlite3
import random
import string
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/hk/Documents/Team2051/'
ALLOWED_EXTENSIONS = set(['csv', 'txt'])



# Database


app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = id_generator() + '.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = sqlite3.connect('2051.db')
            c = conn.cursor()
            data = (filename,'test')
            c.execute('INSERT INTO files(filename, details) VALUES (?,?)', data)
            conn.commit()
            conn.close()
            return render_template('finished.html')

    return render_template('upload.html')



@app.route('/view/<filename>')
def show_dataset(filename):
    error = 0
    conn = sqlite3.connect('2051.db')
    conn.set_trace_callback(print)
    c = conn.cursor()
    print(filename)
    c.execute('SELECT * FROM files WHERE filename=?', (str(filename),))


    if c.fetchone() is None:

        return '''No such file exists'''


    # Open CSV and show data

    dataframe = read_csv('/Users/hk/Documents/Team2051/' + filename)
    print(dataframe)

    df_html = dataframe.to_html()

    return df_html



@app.route('/train/<filename>')
def train_data(filename):

    return 'lol'






@app.route('/')
def hello_world():
    conn = sqlite3.connect('2051.db')
    c = conn.cursor()
    c.execute('SELECT * FROM files')
    query = c.fetchall()
    print(query)
    return render_template('index.html', c=c)

if __name__ == '__main__':
    app.run()
