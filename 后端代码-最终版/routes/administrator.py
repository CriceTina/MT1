from flask import Blueprint, request, jsonify

from services.administrator import findBySearch
from services.administrator import admin_login, get_all_users, update, delete_data
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


@administrator.route('/findBySearch', methods=['POST'])
def findbySearch():
    data = json.loads(request.data)
    userName = data.get('userName')
    pageSize = data.get('pageSize')
    pageNum = data.get('pageNum')
    print("接收到的管理员查询用户的参数:" + userName + "," + str(pageSize) + "," + str(pageNum))

    response = findBySearch(userName, pageSize, pageNum)
    return response


@administrator.route('/edit', methods=['POST'])
def edit():
    data = json.loads(request.data)
    form = data.get('form')
    print("接收到的管理员参数：" + str(form))
    response = update(form)
    return response


@administrator.route('/delete', methods=['POST'])
def delete():
    data = json.loads(request.data)
    ID = data.get('delete_id')
    print("接收到的ID" + str(ID))
    response = delete_data(ID)
    return response





