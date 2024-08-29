from flask import Blueprint, request, jsonify
from services.user import user_register, user_login

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = request.json  # 从请求中获取 JSON 数据
    username = data.get('username')  # 获取用户名
    password = data.get('password')  # 获取密码

    if not username or not password:
        return jsonify({"message": "用户名和密码为必填项"}), 400  # 检查是否提供用户名和密码

    response = user_login(username, password)  # 调用用户登录函数
    return response  # 返回登录结果


@user.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "用户名和密码为必填项"}), 400

    response, status_code = user_register(username, password)
    return jsonify(response), status_code
