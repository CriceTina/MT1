from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from models.UserFeedback import UserFeedback
from flask import jsonify
from models.UserFeedback import db


def findBySearch(feedbackTitle, pageSize, pageNum):
    # 使用 like 操作符进行模糊搜索，% 是通配符，代表任意字符
    # pageSize 是每页显示的记录数，pageNum 是页码
    feedbacks_query = UserFeedback.query.filter(UserFeedback.feedback_title.like(f'%{feedbackTitle}%'))

    # 使用 paginate 方法进行分页
    paginated_feedbacks = feedbacks_query.paginate(page=pageNum, per_page=pageSize, error_out=False)

    # 构建用户反馈信息列表
    feedbacks_info = [
        {
            "feedback_id": feedback.feedback_id,
            "user_id": feedback.user_id,
            "feedback_type": feedback.feedback_type,
            "feedback_title": feedback.feedback_title,
            "feedback_content": feedback.feedback_content,
            "attachment": feedback.attachment,
            "feedback_status": feedback.feedback_status,
            "feedback_time": feedback.feedback_time.strftime("%Y-%m-%d %H:%M:%S")
        } for feedback in paginated_feedbacks.items
    ]

    # 构建响应数据，包括用户反馈信息列表、总页数、当前页码、每页显示的记录数以及总记录数
    response_data = {
        "total_pages": paginated_feedbacks.pages,
        "current_page": pageNum,
        "per_page": pageSize,
        "total": paginated_feedbacks.total,
        "feedbacks": feedbacks_info
    }

    return jsonify(response_data), 200


def delete_data(ID):
    # 查询特定反馈ID的记录
    feedback_to_delete = UserFeedback.query.get(ID)

    if not feedback_to_delete:
        return jsonify({"error": "Feedback not found"}), 404

    # 删除记录
    db.session.delete(feedback_to_delete)
    db.session.commit()

    return jsonify({"success": "Feedback deleted successfully"}), 200


def update(form):
    # 查询特定反馈ID的记录
    feedback_to_update = UserFeedback.query.get(form['feedback_id'])

    if not feedback_to_update:
        return jsonify({"error": "Feedback not found"}), 404

    # 更新记录的字段，以下字段根据实际情况来更新
    feedback_to_update.feedback_type = form.get('feedback_type', feedback_to_update.feedback_type)
    feedback_to_update.feedback_title = form.get('feedback_title', feedback_to_update.feedback_title)
    feedback_to_update.feedback_content = form.get('feedback_content', feedback_to_update.feedback_content)
    feedback_to_update.attachment = form.get('attachment', feedback_to_update.attachment)
    feedback_to_update.feedback_status = form.get('feedback_status', feedback_to_update.feedback_status)
    # 注意：通常不更新创建时间，但如果需要，可以像这样更新
    # feedback_to_update.feedback_time = datetime.strptime(form.get('feedback_time'), "%Y-%m-%d %H:%M:%S")

    # 提交数据库更新
    db.session.commit()

    return jsonify({"success": "Feedback updated successfully"}), 200


def create_userFeedback( feedback_type, feedback_title, feedback_content,user_id):
    new_feedback = UserFeedback(

        feedback_type=feedback_type,
        feedback_title=feedback_title,
        feedback_content=feedback_content,
        feedback_time=datetime.utcnow(),
        user_id=user_id,
        feedback_status="未受理"
    )

    # 保存到数据库
    db.session.add(new_feedback)
    db.session.commit()

    return new_feedback.to_dict()


