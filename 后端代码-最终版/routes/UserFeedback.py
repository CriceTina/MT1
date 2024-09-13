from flask import Blueprint, request, jsonify
import json

from services.UserFeedback import findBySearch, delete_data, update, create_userFeedback

UserFeedback = Blueprint('UserFeedback', __name__)


@UserFeedback.route('/findBySearch', methods=['POST'])
def findbySearch():
    data = json.loads(request.data)
    feedbackTitle = data.get('feedbackTitle')
    pageSize = data.get('pageSize')
    pageNum = data.get('pageNum')
    print("接收到的管理员查询用户的参数:" + feedbackTitle + "," + str(pageSize) + "," + str(pageNum))

    response = findBySearch(feedbackTitle, pageSize, pageNum)
    return response


@UserFeedback.route('/delete', methods=['POST'])
def delete():
    data = json.loads(request.data)
    ID = data.get('delete_id')
    print("接收到的ID" + str(ID))
    response = delete_data(ID)
    return response


@UserFeedback.route('/edit', methods=['POST'])
def edit():
    data = json.loads(request.data)
    form = data.get('form')
    print("接收到的管理员参数：" + str(form))
    response = update(form)
    return response


@UserFeedback.route('/send_feedback', methods=['POST'])
def send_feedback():

    data = request.get_json()

    feedback_type = data.get('feedback_type')
    feedback_title = data.get('feedback_title')
    feedback_content = data.get('feedback_content')
    user_id = data.get('user_id')

    # 检查请求数据

    # 调用业务逻辑层发送通知给所有用户
    create_userFeedback(feedback_type, feedback_title, feedback_content, user_id)

    print("接收到的反馈参数:", feedback_type, feedback_title, feedback_content)
    return jsonify({"message": "反馈已发送"}), 200


