from models.administrator import db
from models.administrator import Administrator
from flask import jsonify
from models.user import db
from models.user import User


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


def get_all_users():
    # 查询所有用户
    users = User.query.all()
    users_info = [{"id": user.user_id,
                   "username": user.username,
                   'registration_time': user.registration_time,
                   'last_login_time': user.last_login_time,
                   'preferred_language_id': user.preferred_language_id,
                   'primary_language_id': user.primary_language_id
                   } for user in users]
    return jsonify(users_info), 200
