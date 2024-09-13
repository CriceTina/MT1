from datetime import date, datetime
from flask import Blueprint, render_template, request, jsonify, send_file

import os

from flask import send_from_directory

from text_model import process_text, insert_translation

bp = Blueprint('file', __name__, url_prefix='/', template_folder='../views/templates')


@bp.route('/file', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            # Read the file content
            file_content = file.read().decode('utf-8')

            # You should validate and sanitize file_content here

            # Process the text
            language = request.form.get('language', 'english')  # Default to English
            language_codes = {
                'english': "en",
                'chinese': "zh",
                'russian': "ru"
            }

            processed_text = process_text(file_content, language_codes[language])

            # Save the processed text to a file
            output_filename = f"processed_{os.path.basename(file.filename)}"
            output_file_path = os.path.join('app/translated_file/', output_filename)
            current_date = date.today()
            now_time = datetime.combine(current_date, datetime.min.time())
            insert_translation(file.filename, output_filename, now_time)
            with open(output_file_path, 'w') as output_file:
                output_file.write(processed_text)

            # Return the path to the processed file
            return jsonify({'download_url': f'http://127.0.0.1:5000/download/{output_filename}'}), 200

    return render_template('file.html')


@bp.route('/download/<filename>')
def download_file(filename):
    # 尝试发送文件，如果文件不存在或发送过程中出现错误，返回错误信息
    file_path = os.path.join('translated_file/', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)
