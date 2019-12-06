from flask import render_template, request, redirect, session, Blueprint

from view_file.auxiliary import url_path_dict

logout_blue = Blueprint('logout_blue', __name__)
@logout_blue.route('/logout/', methods=['Get'])
def logout_view_fun():  # 登出时的视图函数
    if session.get('already_logged_in'):
        session.clear()
        return redirect(url_path_dict['login'])

    return render_template('login_page.html')  # 从后端传到前端, 用对象渲染页面后返回该页面
