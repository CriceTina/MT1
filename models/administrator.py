from config import db_init as db


class Administrator(db.Model):
    __tablename__ = 'administrator'  # 指定表名
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 管理员ID
    adminName = db.Column(db.String(60), nullable=False)  # 管理员名
    adminPassword = db.Column(db.String(200), nullable=False)  # 管理员密码

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'adminName': self.adminName,
            'adminPassword': self.adminPassword
        }
