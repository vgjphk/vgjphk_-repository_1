from flask import render_template, request, flash, session, redirect
from flask import Blueprint
from time import sleep

from view_file.auxiliary import is_in_table_users, add_to_table_users, url_path_dict, is_admin


register_blue = Blueprint('register_blue', __name__)
@register_blue.route('/register/', methods=['Get','POST'])
def register_view_fun():   #注册页面的视图函数
    if request.method == 'POST':
        username = request.form.get('username')             # 获取输入的用户名
        password1 = request.form.get('password1')            # 获取输入的密码
        password2 = request.form.get('password2')            # 获取输入的确认密码
        validate_code = request.form.get('validate_code')    # 获取输入的验证码

        if not validate_code:
            flash('请输入验证码')
        elif not username:
            flash('请输入用户名')
        elif not password1:
            flash('请输入密码')
        elif not password2:
            flash('请确认密码')
        else:           #若用户输入了用户名, 密码, 确认密码和验证码
            if validate_code == session.get('validate_strs'):              #若验证码正确
                if password1==password2:                                   #若密码与确认密码相同
                    if is_in_table_users(username):
                        flash('该用户已存在')
                    else:       #若该用户不存在, 则添加到数据库, 并让其登陆
                        session['already_logged_in'] = True
                        session['username'] = username
                        session['admin'] = False
                        add_to_table_users(username, password1)
                        sleep(3)                #延时3秒, 希望能在网页上有倒计时, 希望前端的同志能添加倒计时
                        return redirect(url_path_dict['home'])  # 已登录, 重定向到主页
                else:
                    flash('密码不一致')
            else:
                flash('验证码不正确')

    return render_template('register_page.html')    #从后端传到前端, 用对象渲染页面后返回该页面