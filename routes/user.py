from flask import Blueprint, request, jsonify, session
from services.user import user_register, user_login, user_change_password
from models.user import db
from models.user import User


user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
def register():
    # 从请求中获取表单数据
    username = request.form.get('username')
    password = request.form.get('password')

    print("接收到的用户注册参数:", username, password)

    response = user_register(username, password)  # 调用用户注册函数
    return response


@user.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')  # 从请求中获取表单数据
    password = request.form.get('password')  # 获取密码

    print("接收到的用户登录参数:", username, password)

    response = user_login(username, password)  # 调用用户登录函数
    return response  # 返回登录结果


@user.route('/change-password', methods=['POST'])
def change_password():
    if 'username' not in session:
        return jsonify({"message": "用户未登录"}), 403

    # 查找当前用户
    current_user = User.query.get(session['username'])

    # 获取表单数据
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')

    return user_change_password(current_user, new_password1, new_password2)
