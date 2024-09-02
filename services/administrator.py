from models.administrator import db
from models.administrator import Administrator
from flask import jsonify


def admin_login(adminName, adminPassword):
    admin = Administrator.query.filter_by(adminName=adminName).first()
    if admin is None:
        # 管理员不存在
        return jsonify({
            'code': -1,
            "message": "管理员不存在",
            "data": ""
        }), 201
    admin_dict = admin.to_dict()

    if admin_dict['adminPassword'] != adminPassword:
        # 管理员存在 密码错误
        return jsonify({
            'code': -2,
            "message": "密码错误",
            "data": ""
        }), 202

    return jsonify({
        'code': 0,
        "message": "登录成功",
        "data": admin_dict
    })
