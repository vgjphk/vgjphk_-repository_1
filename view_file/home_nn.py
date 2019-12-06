from flask import render_template, session, redirect
from flask import Blueprint

from view_file.auxiliary import url_path_dict, read_table_columns, sort_by_col
from config_file import db_parameter


def get_data_home1():  # 筛选出'今日'的所需数据并按时间升序排列
    a = read_table_columns(db_parameter['table_name'],
                           '统计时间',
                           '所属街道',
                           '所属社区',
                           '问题来源',
                           '小类名称',
                           '问题性质名称',
                           '处置部门')
    temp = []
    for i in range(len(a[0])):
        if a[0][i][:10] == '2018-10-30':
            temp.append(i)
    b = [[], [], [], [], [], [], []]
    for i in range(len(b)):
        for j in temp:
            b[i].append(a[i][j])
    del a
    b = sort_by_col(b, 0)
    return b


def get_data_home2():  # 筛选出自定义异常事件的所需数据并按时间升序排列
    a = read_table_columns(db_parameter['table_name'],
                           '统计时间',  # 必有
                           '所属街道',
                           '所属社区',
                           '问题来源',  # 必有
                           '小类名称',  # 必有
                           '问题性质名称')
    temp = []
    for i in range(len(a[0])):
        if a[5][i] == '-':
            temp.append(i)
    b = [[], [], [], [], []]
    for i in [0, 3, 4]:
        for j in temp:
            b[i].append(a[i][j])
    for j in temp:
        if a[1][j] == '-':
            b[1].append('未知街道')
        else:
            b[1].append(a[1][j])
    for j in temp:
        if a[2][j] == '-':
            b[2].append('未知社区')
        else:
            b[2].append(a[2][j])
    del a
    b = sort_by_col(b, 0)
    return b


home_blue = Blueprint('home_blue', __name__)


@home_blue.route('/home/', methods=['Get'])
def home_view_fun():  # 主页的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    data1 = get_data_home1()
    index_list = [x for x in range(len(data1[0]))]

    if not session['admin']:
        return render_template('ordinary_home_page.html', data1=data1, index_list=index_list)  # 从后端传到前端,
        # 用对象渲染页面后返回该页面
    if session['admin']:
        return render_template('home_page.html', data1=data1, index_list=index_list)  # 从后端传到前端, 用对象渲染页面后返回该页面


@home_blue.route('/home/more/', methods=['Get'])
def home_more_view_fun():  # 主页的更多的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    data = get_data_home1()
    index_list = [x for x in range(len(data[0]))]
    return render_template('home_more_page.html', data=data, index_list=index_list)  # 从后端传到前端, 用对象渲染页面后返回该页面


@home_blue.route('/home/zdy/', methods=['Get'])
def home_zdy_view_fun():  # 主页的自定义异常事件的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    data2 = get_data_home2()
    index_list = [x for x in range(len(data2[0]))]
    if session['admin']:
        return render_template('home_zdy_page.html', data2=data2, index_list=index_list)  # 从后端传到前端, 用对象渲染页面后返回该页面
    else:
        return render_template('ordinary_home_zdy_page.html', data2=data2, index_list=index_list)  # 从后端传到前端, 用对象渲染页面后返回该页面
