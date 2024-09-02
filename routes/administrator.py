from flask import Blueprint, request, jsonify
from services.administrator import admin_login

administrator = Blueprint('administrator', __name__)


@administrator.route('/login', methods=['POST'])
def login():
    adminName = request.form.get('adminName')  # 从请求中获取表单数据
    adminPassword = request.form.get('adminPassword')  # 获取密码

    print("Received data:", adminName, adminPassword)

    response = admin_login(adminName, adminPassword)  # 调用用户登录函数
    return response  # 返回登录结果
