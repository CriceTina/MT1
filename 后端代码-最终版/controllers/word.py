from flask import Flask, request, jsonify, Blueprint, render_template

from wordcontent import get_word_data, format_output

bp = Blueprint('word', __name__, url_prefix='/', template_folder='../views/templates')


@bp.route('/word', methods=['POST', 'GET'])
def process_word():
    if request.method == 'POST':
        word = request.json.get('word', '')
        if not word:
            return jsonify({'error': 'No word provided'}), 400
        word_data = get_word_data(word)
        word_data = format_output(word_data)

        return jsonify(word_data)

    return render_template('word.html')
