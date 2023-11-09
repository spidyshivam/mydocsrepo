from flask import Flask, render_template, redirect, request, send_from_directory
import os
import time

UPLOAD_FOLDER = '/home/shivam/data'

#Flask Config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 10


# Listing Files and their creation time from server
def get_file_info():
    file_list = os.listdir(UPLOAD_FOLDER)
    file_info = {}
    for filename in file_list:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            file_stats = os.stat(file_path)
            creation_time = file_stats.st_ctime
            formatted_creation_time = f"{time.ctime(creation_time)}"
            file_info[filename] = formatted_creation_time
            file_info = dict(sorted(file_info.items(), key=lambda item: item[1], reverse=True))
    return file_info


#Routes
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        try:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(file.filename))
            file.save(filename)
            return redirect('/')
        except:
            return "Error in uploading the file!"
    else:
        return render_template('index.html', file_info=get_file_info())

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
