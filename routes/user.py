from flask import Blueprint, request, jsonify
from services.user import user_register, user_login

user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
def register():
    # 从请求中获取表单数据
    username = request.form.get('username')
    password = request.form.get('password')

    response = user_register(username, password)  # 调用用户注册函数
    return response


@user.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')  # 从请求中获取表单数据
    password = request.form.get('password')  # 获取密码

    response = user_login(username, password)  # 调用用户登录函数
    return response  # 返回登录结果
