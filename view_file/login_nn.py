from flask import render_template, request, flash, redirect, session, Blueprint
from sqlalchemy import and_

from view_file.auxiliary import url_path_dict, is_admin


login_blue = Blueprint('login_blue', __name__)
@login_blue.route('/', methods=['Get','POST'])
@login_blue.route('/login/', methods=['Get','POST'])
def login_view_fun():   #登陆时的视图函数
    if session.get('already_logged_in') == True:
        return redirect(url_path_dict['home'])      #已登录, 重定向到主页

    if request.method == 'POST':
        username = request.form.get('username')                 #获取输入的用户名
        password = request.form.get('password')                 #获取输入的密码
        validate_code = request.form.get('validate_code')       #获取输入的验证码

        if not validate_code:
            flash('请输入验证码')
        elif not username:
            flash('请输入用户名')
        elif not password:
            flash('请输入密码')
        else:           #若用户输入了用户名, 密码和验证码
            from db_models.user_model import User                   # 从数据库中提取用户, 在此处导入可避免循环导入
            a_user = User.query.filter(and_(User.name == username, User.password == password)).all()

            if validate_code == session.get('validate_strs'):              #若验证码正确
                if not a_user == []:                            #若用户名和密码都正确
                    session['already_logged_in'] = True
                    session['username'] = username
                    session['admin'] = True if is_admin(username) else False
                    return redirect(url_path_dict['home'])      #登陆成功重定向到主页
                else:
                    flash('用户名或密码错误')
            else:
                flash('验证码不正确')

    return render_template('login_page.html')    #从后端传到前端, 用对象渲染页面后返回该页面


