from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from models.user import db
from routes.user import user
from models.administrator import db
from routes.administrator import administrator
from models.systemnotification import db
from routes.systemnotification import ss
from config import app

import os
from datetime import timedelta
from flask_cors import CORS

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保创建数据库表
    # app.run(host='0.0.0.0', port=5000, debug=True)

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
