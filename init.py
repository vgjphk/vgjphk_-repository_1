from flask import Flask
from datetime import timedelta

# 导入配置文件
from config_file import config_app

# 导入视图文件, 用于注册蓝本
from view_file.auxiliary import auxiliary_blue
from view_file.login_nn import login_blue
from view_file.home_nn import home_blue
from view_file.register_nn import register_blue
from view_file.jrms import jrms_blue
from view_file.mssj import mssj_blue
from view_file.rdsq import rdsq_blue
from view_file.sjjb import sjjb_blue
from view_file.search import search_blue
from view_file.my_home import my_home_blue
from view_file.logout import logout_blue
from view_file.event_input import event_input_blue
from view_file.progress_update import progress_update_blue


def create_app():
    # 创建flask对象实例app
    app = Flask(__name__)

    # 进行相关配置
    config_app(app)

    # 修改静态文件缓存时间，相当于不缓存
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

    # 注册蓝本, 可以加第二个参数url_prefix ='/随意字符', 此时网址就要加此前缀
    app.register_blueprint(auxiliary_blue)
    app.register_blueprint(login_blue)
    app.register_blueprint(home_blue)
    app.register_blueprint(register_blue)
    app.register_blueprint(jrms_blue)
    app.register_blueprint(mssj_blue)
    app.register_blueprint(rdsq_blue)
    app.register_blueprint(sjjb_blue)
    app.register_blueprint(my_home_blue)
    app.register_blueprint(search_blue)
    app.register_blueprint(logout_blue)
    app.register_blueprint(event_input_blue)
    app.register_blueprint(progress_update_blue)

    return app
