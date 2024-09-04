from flask import Blueprint, request, jsonify
from services.administrator import admin_login, get_all_users
import json


administrator = Blueprint('administrator', __name__)


@administrator.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    adminName = data.get('adminName')  # 从请求中获取表单数据
    adminPassword = data.get('adminPassword')  # 获取密码

    print("接收到的管理员登录参数:", adminName, adminPassword)

    response = admin_login(adminName, adminPassword)  # 调用管理员登录函数
    return response  # 返回登录结果


@administrator.route('/view_users', methods=['POST'])
def view_users():
    return get_all_users()

