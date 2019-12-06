from flask import render_template, request, flash, session, redirect
from flask import Blueprint
from view_file.auxiliary import url_path_dict

progress_update_blue = Blueprint('progress_update_blue', __name__)


@progress_update_blue.route('/progress_update/', methods=['Get', 'POST'])
def progress_update_view_fun():  # 个人中心的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    if not session['admin']:  # 防止普通用户直接跳转到事件进度更新页面，只有管理员有此权限
        return redirect(url_path_dict['home'])
    if request.method == 'POST':
        num = request.form.get('num')   # 获取输入编号
        progress = request.form.get('progress')  # 获取输入编号
        if not num:
            flash('请输入事件编号')
        elif not progress:
            flash('请输入当前进度')
        else:  # 若用户完成输入
            from view_file.auxiliary import search_by_num, change_progress
            target = search_by_num(num)
            if not target:
                flash('不存在此事件:请重新输入事件编号！')
            else:
                if target[21] != '1':
                    flash('事件已办结完成！无法更改事件进度！')
                else:
                    change_progress(target,progress)
                    flash('更新成功！')
    return render_template('progress_update_page.html')  # 从后端传到前端, 用对象渲染页面后返回该页面
