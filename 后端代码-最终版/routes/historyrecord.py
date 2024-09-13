from flask import Blueprint, request, jsonify, session
from models.historyrecord import db
from models.historyrecord import Historyrecord

historyrecord = Blueprint('historyrecord', __name__)


@historyrecord.route('/user_query_history', methods=['POST'])
def get_user_history():

    user_id = request.json.get('user_id')

    # 检查用户是否登录
    if user_id is None:
        return jsonify({
            'code': -1,
            'message': '用户未登录',
            'data': []
        }), 401  # 返回未授权状态码

    # 查询当前用户的所有历史记录
    history_records = Historyrecord.query.filter_by(user_id=user_id).all()

    # 将历史记录转换为字典格式
    history_records_list = [record.to_dict() for record in history_records]

    return jsonify({
        'code': 0,
        'message': '成功获取历史记录',
        'data': history_records_list
    }), 200  # 返回成功状态码


