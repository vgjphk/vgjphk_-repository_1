from flask import render_template, request, flash, session, redirect
from flask import Blueprint
from view_file.auxiliary import url_path_dict

event_input_blue = Blueprint('event_input_blue', __name__)  # my_home个人中心


@event_input_blue.route('/event_input/', methods=['Get', 'POST'])
def event_input_view_fun():  # 个人中心的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    if not session['admin']:  # 防止普通用户直接跳转到事件输入页面，只有管理员有此权限
        return redirect(url_path_dict['home'])
    if request.method == 'POST':
        num = request.form.get('num')   # 获取输入编号
        date = request.form.get('date')  # 获取输入的日期
        area = request.form.get('area')  # 获取所属区域
        street = request.form.get('street')  # 获取输入的街道
        community = request.form.get('community')  # 获取输入的社区
        types = request.form.get('types')  # 获取输入的问题类型
        big_type = request.form.get('big_type')  # 获取输入的大类名称
        tiny_type = request.form.get('tiny_type')  # 获取输入的小类名称
        department = request.form.get('department')  # 获取输入的处置部门
        way = request.form.get('way')  # 获取输入的问题来源
        progress = request.form.get('progress')  # 获取输入的事件进度
        nature = request.form.get('nature')  # 获取输入的问题性质
        print(types)
        if not num:
            flash('请输入编号')
        elif not date:
            flash('请输入日期')
        elif not area:
            flash('请输入所属区域')
        elif not street:
            flash('请输入问题街道')
        elif not community:
            flash('请输入问题社区')
        elif not types:
            flash('请输入问题类型')
        elif not big_type:
            flash('请输入大类名称')
        elif not tiny_type:
            flash('请输入小类名称')
        elif not department:
            flash('请输入处置部门')
        elif not way:
            flash('请输入问题来源')
        elif not progress:
            flash('请输入事件进度')
        elif not nature:
            flash('请输入事件性质')
        else:  # 若用户完成输入
            from view_file.auxiliary import write_to_db, if_exist
            if if_exist(date, area, street, community, types, big_type, tiny_type, way, nature):
                print(if_exist(date, area, street, community, types, big_type, tiny_type, way, nature))
                flash('此条数据已存在！')
            else:
                write_to_db(num, date, area, street, community, types, big_type, tiny_type, department, way, progress, nature)
                flash('添加完成！')
    return render_template('event_input_page.html')  # 从后端传到前端, 用对象渲染页面后返回该页面
