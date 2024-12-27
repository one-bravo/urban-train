import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory

app = Flask(__name__)

# Create an upload folder in the same directory as app.py
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index'))

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(url_for('index'))

        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return redirect(url_for('index'))

    # List existing files in the uploads folder
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
