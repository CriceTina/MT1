from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/mt'

# 数据库连接对象
db_init = SQLAlchemy(app)

