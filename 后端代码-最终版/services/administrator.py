from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

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


def findBySearch(userName, pageSize, pageNum):
    # 使用 like 操作符进行模糊搜索，% 是通配符，代表任意字符
    # pageSize 是每页显示的记录数，pageNum 是页码
    users_query = User.query.filter(User.username.like(f'%{userName}%'))

    # 使用 paginate 方法进行分页
    paginated_users = users_query.paginate(page=pageNum, per_page=pageSize, error_out=False)

    # 构建用户信息列表
    users_info = [
        {
            "id": user.user_id,
            "username": user.username,
            'registration_time': user.registration_time,
            'last_login_time': user.last_login_time,
            'preferred_language_id': user.preferred_language_id,
            'primary_language_id': user.primary_language_id
        } for user in paginated_users.items
    ]

    # 构建响应数据，包括用户信息列表、总页数、当前页码、每页显示的记录数以及总记录数
    response_data = {
        "total_pages": paginated_users.pages,
        "current_page": pageNum,
        "per_page": pageSize,
        "total": paginated_users.total,
        "users": users_info
    }

    return jsonify(response_data), 200


def update(form):
    # 提取form中的ID
    user_id = form['id']

    # 转换注册时间和最后登录时间的字符串为datetime对象
    registration_time = datetime.strptime(form['registration_time'], '%a, %d %b %Y %H:%M:%S %Z')
    last_login_time = datetime.strptime(form['last_login_time'], '%a, %d %b %Y %H:%M:%S %Z')

    # 构建更新SQL语句
    # 注意：这里假设注册时间、最后登录时间、首选语言ID和主要语言ID字段都需要更新
    # 如果不需要更新某个字段，可以省略相应的更新语句
    update_data = {
        'last_login_time': last_login_time,
        'preferred_language_id': form['preferred_language_id'],
        'primary_language_id': form['primary_language_id'],
        'registration_time': registration_time,
        'username': form['username']
    }

    # 构建更新条件
    where_condition = User.user_id == user_id

    # 执行更新操作
    db.session.query(User).filter(where_condition).update(update_data)
    db.session.commit()

    # 返回成功消息
    return jsonify({"success": "User update successfully"}), 200


def delete_data(ID):
    # 构建删除条件
    where_condition = User.user_id == ID

    try:
        # 执行删除操作
        db.session.query(User).filter(where_condition).delete()
        db.session.commit()
        # 返回成功消息
        return jsonify({"success": "User deleted successfully"}), 200
    except SQLAlchemyError as e:
        # 如果发生错误，回滚事务并返回错误消息
        db.session.rollback()
        return f"An error occurred: {str(e)}", 500


