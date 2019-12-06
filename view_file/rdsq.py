from flask import render_template, request, redirect, session
from flask import Blueprint
import json
import pymysql
import pandas as pd

from config_file import today, db_parameter
from view_file.auxiliary import url_path_dict, sort_by_col


def read_date_rdsq(date_begin, date_end, num=0):
    '''
    :param date_begin: 起始时间
    :param date_end: 终止时间
    :param num: 若data_end为今日, 则过去的数据照常返回, 今日当天只返回num行, 若今日不足num行, 则只返回今日数据
    :return: 符合要求的数据
    '''
    if date_end < today:
        date_end += ' 23:59:59'
    elif date_end == today:
        mysql_command2 = "select 统计时间, 所属社区 from " + db_parameter['table_name'] + " where 统计时间>'" + \
                         today + "'and 统计时间<'" + today + " 23:59:59" + "';"
    else:
        raise Exception

    mysql_command = "select 所属社区 from " + db_parameter['table_name'] + " where 统计时间>'" + \
                    date_begin + "'and 统计时间<'" + date_end + "';"
    cursor = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                             password=db_parameter['db_password'],
                             db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                             charset=db_parameter['character_set'])
    dd_rdsq = list(pd.read_sql(mysql_command, con=cursor)['所属社区'])
    if date_end == today:
        di = pd.read_sql(mysql_command2, con=cursor)  # 读取今日数据
        tt = sort_by_col([list(di['统计时间']), list(di['所属社区'])])
        dd_rdsq.extend(tt[1][:num])

    num_list = [0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0]
    sq_name_list = ['马峦社区', '金龟社区', '汤坑社区', '江岭社区', '坪环社区', '坪山社区',
                    '沙坣社区', '六联社区', '田头社区', '碧岭社区', '沙湖社区', '田心社区',
                    '六和社区', '竹坑社区', '老坑社区', '坑梓社区', '和平社区', '石井社区',
                    '南布社区', '金沙社区', '龙田社区', '沙田社区', '秀新社区']
    for i in dd_rdsq:
        if i not in sq_name_list:
            continue
        a_index = sq_name_list.index(i)
        num_list[a_index] += 1
    for i in range(len(num_list)):  # 优化地图上点的大小
        if num_list[i] != 0:
            num_list[i] = num_list[i] * 2 + 100
    return num_list


rdsq_blue = Blueprint('rdsq_blue', __name__)  # rdsq是热点社区的拼音首字母


@rdsq_blue.route('/rdsq/', methods=['Get', 'POST'])
def rdsq_view_fun():  # 热点社区分析的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    from config_file import today
    date_begin = date_end = today

    if request.method == 'POST':  # 得到新的日期范围, 需要必要的检查
        date_begin = request.form.get('start')
        date_end = request.form.get('end')
    if not (date_begin <= date_end <= today):
        return redirect(url_path_dict['rdsq'])

    if date_end < today:
        num_list = read_date_rdsq(date_begin, date_end)  # 获取热点社区列表
        need_refresh = 0
    else:
        if session.get('num') == None:
            session['num'] = 0
        session['num'] = session['num'] + 1
        num_list = read_date_rdsq(date_begin, date_end, session['num'])  # 获取热点社区列表
        need_refresh = 1

    if session['admin']:
        return render_template('rdsq_page.html', num_list_json=json.dumps(num_list),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
    if not session['admin']:
        return render_template('ordinary_rdsq_page.html', num_list_json=json.dumps(num_list),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
