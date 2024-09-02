from flask import Flask, jsonify
from models.user import db
from routes.user import user
from models.administrator import db
from routes.administrator import administrator
from config import app
from flask import request

from flask_cors import CORS

# 创建 Flask 应用实例
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/mt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# 注册用户、管理员蓝图
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(administrator, url_prefix="/administrator")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保创建数据库表
    app.run(host='0.0.0.0', port=5000, debug=True)
