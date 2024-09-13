from datetime import date, datetime
from flask import Blueprint, render_template, request, jsonify

from text_model import process_text, insert_translation

bp = Blueprint('text', __name__, url_prefix='/', template_folder='../views/templates')


@bp.route('/text', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        language = request.form.get('language', 'english')  # Default to English
        language_codes = {
            'english': "en",
            'chinese': "zh",
            'russian': "ru"
        }

        if language not in language_codes:
            return jsonify({'error': 'Unsupported language'}), 400

        processed_text = process_text(input_text, language_codes[language])
        current_date = date.today()
        now_time = datetime.combine(current_date, datetime.min.time())
        insert_translation(input_text, processed_text, now_time)

        return jsonify({'processed_text': processed_text})

    return render_template('text.html')
