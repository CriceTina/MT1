from flask import Flask, jsonify
from models.user import db
from routes.user import user
from config import app
from flask import request

# 创建 Flask 应用实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/mt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 注册用户蓝图
app.register_blueprint(user, url_prefix="/user")


@app.route('/')
def ping():
    return 'ok'


# 测试用户注册
@app.route('/user/register', methods=['POST'])
def test_register():
    # 从请求中获取 JSON 数据
    test_data = request.get_json()

    with app.test_client() as client:
        # 发送 POST 请求到 '/user/register'
        response = client.post('/user/register', json=test_data)
        return jsonify(response.get_json()), response.status_code


# 测试用户登录
@app.route('/user/login', methods=['POST'])
def test_login():
    # 从请求中获取 JSON 数据
    test_data = request.get_json()

    if not test_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    with app.test_request_context('/user/login', method='POST', json=test_data):
        response = user.login()
        return jsonify(response.get_json()), response.status_code


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保创建数据库表
    app.run(host='0.0.0.0', port=5000, debug=True)
