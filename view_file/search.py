from flask import render_template, request, flash, Blueprint,session,redirect
from view_file.auxiliary import url_path_dict

search_blue = Blueprint('search_blue', __name__)


@search_blue.route('/search/', methods=['Get', 'POST'])
def search_view_fun():  # 查询时的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    target_event = {}
    if request.method == 'POST':
        date = request.form.get('date')  # 获取输入的日期
        way = request.form.get('way')  # 获取输入的问题来源
        community = request.form.get('community')  # 获取输入的社区
        street = request.form.get('street')  # 获取输入的街道
        nature = request.form.get('nature')  # 获取输入的问题性质
        if not date:
            flash('请输入日期')
        elif not way:
            flash('请输入投诉渠道')
        elif not community:
            flash('请输入问题社区')
        elif not street:
            flash('请输入问题街道')
        elif not nature:
            flash('请输入事件性质')
        else:  # 若用户完成输入
            from view_file.auxiliary import event_search
            target_event = event_search(date, way, community, street, nature)
            if not target_event:
                flash('查询无结果:请重新输入查询内容')
            else:
                flash('您的查询结果：')
    if not session['admin']:
        return render_template('ordinary_search_page.html', target_event=target_event)  # 从后端传到前端, 用对象渲染页面后返回该页面
    if session['admin']:
        return render_template('search_page.html', target_event=target_event)  # 从后端传到前端, 用对象渲染页面后返回该页面
