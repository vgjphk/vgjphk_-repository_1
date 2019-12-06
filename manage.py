#运行本模块即可启动整个程序
from flask_sqlalchemy import SQLAlchemy

from init import create_app

app = create_app()

#定义数据库对象db
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)

