from io import BytesIO

from PIL import Image
from flask import Flask, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from pytesseract import pytesseract
from sympy.physics.units import sr
import ffmpeg
import subprocess

from ai_model import llama3
from routes.BackendData import BackendData
from routes.UserFeedback import UserFeedback
from routes.user import user
from models.administrator import db
from routes.administrator import administrator
from models.systemnotification import db
from routes.systemnotification import ss
from models.historyrecord import db
from models import historyrecord
from routes.historyrecord import historyrecord

import base64
from io import BytesIO
from flask import request, jsonify

from config import app
from datetime import datetime, date

import os
from datetime import timedelta
from flask_cors import CORS

from services.historyrecord import create_history_record
from text_model import process_text, read_text_file, change_file_extension
from video_model import process_audio
from wordcontent import get_word_data, format_output

# 创建 Flask 应用实例
app = Flask(__name__)
socketio = SocketIO(app)  # 初始化 SocketIO
app.config.from_object(__name__)
app.secret_key = os.urandom(24)  # 随机生成session密钥
app.permanent_session_lifetime = timedelta(minutes=60)  # 设置session时效为60分钟

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/mt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app)

# 注册用户、管理员、系统通知蓝图
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(administrator, url_prefix="/administrator")
app.register_blueprint(ss, url_prefix="/ss")
app.register_blueprint(historyrecord, url_prefix="/historyrecord")
app.register_blueprint(UserFeedback, url_prefix="/UserFeedback")
app.register_blueprint(BackendData, url_prefix="/BackendData")


@app.route('/translate_text', methods=['POST'])  # 文本翻译
def translate_text():
    text = request.json.get('text')
    targetlanguage = request.json.get('targetlanguage')
    user_id = request.json.get('user_id')

    # 调用翻译模型进行翻译
    translated_text = process_text(text, targetlanguage)

    # 创建历史记录
    history_record = create_history_record(user_id, text, translated_text, targetlanguage)

    return jsonify({
        'translated_text': translated_text,
        'statusCode': 200
    })


@app.route('/translate_file', methods=('GET', 'POST'))  # 文件翻译
def translate_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        # filePath = request.form['filePath']  # 获取文件路径
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            file_content = file.read().decode('utf-8')

            language = request.form.get('language', 'en')  # Default to English

            processed_text = process_text(file_content, language)

            output_filename = f"processed_{os.path.basename(file.filename)}"
            output_file_path = os.path.join('translated_file/', output_filename)
            current_date = date.today()
            now_time = datetime.combine(current_date, datetime.min.time())
            # insert_translation(file.filename, output_filename, now_time)
            with open(output_file_path, 'w') as output_file:
                output_file.write(processed_text)

            return jsonify({
                'download_url': f'http://192.168.148.26:5000/download/{output_filename}',
                'code': 200
            }), 200


@app.route('/download/<filename>')  # 下载文件
def download_file(filename):
    # 尝试发送文件，如果文件不存在或发送过程中出现错误，返回错误信息
    file_path = os.path.join('translated_file/', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/translate_image', methods=('GET', 'POST'))  # 图片翻译
def translate_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No image part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            language = request.form.get('language', 'en')
            image = Image.open(BytesIO(file.read()))

            input_text = pytesseract.image_to_string(image, lang='chi_sim+eng+rus+chi_tra')

            processed_text = process_text(input_text, language)

            file_name = 'image.txt'

            output_filename = f"processed_{os.path.basename(file_name)}"

            output_file_path = os.path.join('translated_file/', output_filename)

            with open(output_file_path, 'w') as output_file:
                output_file.write(processed_text)

            # Return the path to the processed file
            return jsonify({
                'download_url': f'http://192.168.148.26:5000/download/{output_filename}',
                'code': 200
            }), 200


@app.route('/translate_word', methods=['POST', 'GET'])
def translate_word():
    if request.method == 'POST':
        word = request.json.get('word')
        useid = request.json.get('user_id')
        print(type(word))
        if not word:
            return jsonify({'error': 'No word provided'}), 400
        word_data = get_word_data(word)
        word_data = format_output(word_data)

        return jsonify({'word_data': word_data})


@app.route('/translate_voice', methods=['POST'])
def upload_voice():
    print(request)
    if 'file' not in request.files:
        return {'code': 400, 'msg': 'No file part'}

    file = request.files['file']
    if file.filename == '':
        return {'code': 400, 'msg': 'No selected file'}

    directory = '/tmp/translated_file'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file.filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    file.save(file_path)

    mp3_file_path = os.path.join(directory, 'converted_audio.mp3')

    if os.path.exists(mp3_file_path):
        os.remove(mp3_file_path)

    command = f"ffmpeg -i {file_path} {mp3_file_path}"

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return {'code': 500, 'msg': 'Failed to convert audio', 'error': str(e)}

    text = process_audio(mp3_file_path)

    return jsonify({'code': 200, 'text': text}), 200


@app.route('/translate_ai', methods=('GET', 'POST'))
def ai():
    if request.method == 'POST':
        input_text = request.json.get('input_text')
        print(input_text)
        input_text = str(input_text['value'])
        print(type(input_text))

        processed_text = llama3(input_text)
        print(processed_text)
        return jsonify({'processed_text': processed_text})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保创建数据库表
    app.run(host='0.0.0.0', port=5000, debug=True)
