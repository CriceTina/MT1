
from datetime import date, datetime
from flask import Blueprint, render_template, request, jsonify
from PIL import Image
import pytesseract
from io import BytesIO

from text_model import process_text, insert_translation

bp = Blueprint('image', __name__, url_prefix='/', template_folder='../views/templates')


@bp.route('/image', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image part'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            language = request.form.get('language', 'english')
            image = Image.open(BytesIO(file.read()))

            # Use pytesseract to do OCR on the image
            input_text = pytesseract.image_to_string(image, lang='chi_sim+eng+rus+chi_tra')

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
            insert_translation(file.filename, file.filename, now_time)

            return jsonify({'extracted_text': processed_text})

    return render_template('image.html')




