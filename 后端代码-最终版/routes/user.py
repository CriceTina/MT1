from flask import Blueprint, request, jsonify, session
from services.user import user_register, user_login, user_change_password, session_store
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
    username = request.form.get('username')  # 从请求中获取用户名
    password = request.form.get('password')  # 获取密码
    code = request.form.get('code')  # 从请求中获取微信的 code

    print("接收到的用户登录参数:", username, password, code)

    response = user_login(username, password, code)  # 调用用户登录函数
    return response  # 返回登录结果


@user.route('/change_password', methods=['POST'])
def change_password():
    # 获取请求数据
    data = request.form
    session_id = data.get('id')
    new_password1 = data.get('new_password1')
    new_password2 = data.get('new_password2')

    # 获取用户信息
    user_info = session_store[session_id]
    username = user_info['username']

    # 获取用户对象
    current_user = User.query.filter_by(username=username).first()
    if not current_user:
        return jsonify({'code': 1, 'message': 'User not found'}), 404

    print("接收到的用户修改密码参数:", new_password1, new_password2)

    # 调用业务逻辑层修改密码
    response = user_change_password(current_user, new_password1, new_password2)
    return response


