from flask import render_template, request, flash, session, redirect
from flask import Blueprint

my_home_blue = Blueprint('my_home_blue', __name__)  # my_home个人中心


@my_home_blue.route('/my_home/', methods=['Get', 'POST'])
def my_home_view_fun():  # 个人中心的视图函数
    username = session.get('username')
    assert username is not None
    if not session['admin']:
        return render_template('ordinary_user_my_home_page.html', username=username)  # 从后端传到前端, 用对象渲染页面后返回该页面
    if session['admin']:
        return render_template('admin_my_home_page.html', username=username)  # 从后端传到前端, 用对象渲染页面后返回该页面
