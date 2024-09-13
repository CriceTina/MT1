from config import db_init as db
from datetime import datetime


class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'  # 指定表名

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 反馈ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    feedback_type = db.Column(db.String(100), nullable=False)  # 反馈类型
    feedback_title = db.Column(db.String(200), nullable=False)  # 反馈标题
    feedback_content = db.Column(db.Text, nullable=False)  # 反馈内容
    attachment = db.Column(db.String(200))  # 附件
    feedback_status = db.Column(db.String(50), nullable=False)  # 反馈状态
    feedback_time = db.Column(db.DateTime, default=datetime.utcnow)  # 反馈时间

    def to_dict(self):
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'feedback_type': self.feedback_type,
            'feedback_title': self.feedback_title,
            'feedback_content': self.feedback_content,
            'attachment': self.attachment,
            'feedback_status': self.feedback_status,
            'feedback_time': self.feedback_time.strftime("%Y-%m-%d %H:%M:%S")
        }




