from config import db_init as db
import time


class User(db.Model):
    __tablename__ = 'user'  # 指定表名
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)  # 用户名
    password = db.Column(db.String(255), nullable=False)  # 密码
    registration_time = db.Column(db.DateTime, nullable=True)  # 注册时间
    last_login_time = db.Column(db.DateTime, nullable=True, default=None)  # 最近登录时间
    preferred_language_id = db.Column(db.Integer, nullable=True, default=1)  # 偏好语言ID
    primary_language_id = db.Column(db.Integer, nullable=True, default=1)  # 主语言ID

    def to_dict(self):
        return {

            'user_id': self.user_id,
            'username': self.username,
            'password':self.password,
            'registration_time': self.registration_time,
            'last_login_time': self.last_login_time,
            'preferred_language_id': self.preferred_language_id,
            'primary_language_id': self.primary_language_id
        }
