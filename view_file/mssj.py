from flask import render_template, session, request, redirect
from flask import Blueprint
import json
import pymysql
import pandas as pd

from config_file import today, db_parameter
from view_file.auxiliary import url_path_dict, sort_by_col


def read_date_mssj(date_begin, date_end, num=0):
    '''
    :param date_begin: 起始时间
    :param date_end: 终止时间
    :param num: 若data_end为今日, 则过去的数据照常返回, 今日当天只返回num行, 若今日不足num行, 则只返回今日数据
    :return: 符合要求的数据
    '''
    if date_end < today:
        date_end += ' 23:59:59'
    elif date_end == today:
        mysql_command2 = "select 统计时间, 所属街道, 小类名称 from " + db_parameter['table_name'] + " where 统计时间>'" + \
                         today + "'and 统计时间<'" + today + " 23:59:59" + "';"
    else:
        raise Exception

    mysql_command = "select 所属街道, 小类名称 from " + db_parameter['table_name'] + "  where 统计时间>'" + \
                    date_begin + "'and 统计时间<'" + date_end + "';"
    cursor = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                             password=db_parameter['db_password'],
                             db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                             charset=db_parameter['character_set'])
    di = pd.read_sql(mysql_command, con=cursor)
    dd_mssj = [list(di['所属街道']), list(di['小类名称'])]

    if date_end == today:
        di = pd.read_sql(mysql_command2, con=cursor)  # 读取今日数据
        tt = sort_by_col([list(di['统计时间']), list(di['所属街道']), list(di['小类名称'])])
        dd_mssj[0].extend(tt[1][:num])
        dd_mssj[1].extend(tt[2][:num])

    l_e_table = []  # 民生事件表
    street_name_list = ['马峦街道', '碧岭街道', '石井街道', '坪山街道', '龙田街道', '坑梓街道']  # 街道名称列表(列名表)
    l_e_name_list = []  # 小类名称列表(行名表)
    for i in range(len(dd_mssj[0])):
        if dd_mssj[0][i] not in street_name_list:
            continue
        if not (dd_mssj[1][i] in l_e_name_list):
            l_e_table.append([0, 0, 0, 0, 0, 0])
            l_e_name_list.append(dd_mssj[1][i])
        col_index = street_name_list.index(dd_mssj[0][i])  # 列索引
        row_index = l_e_name_list.index(dd_mssj[1][i])  # 行索引
        l_e_table[row_index][col_index] += 1
    return l_e_table, street_name_list, l_e_name_list


mssj_blue = Blueprint('mssj_blue', __name__)  # mssj是民生事件的拼音首字母


@mssj_blue.route('/mssj/', methods=['Get', 'POST'])
def mssj_view_fun():  # 各街道民生事件情况的视图函数
    if not session.get('already_logged_in'):
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    from config_file import today
    date_begin = date_end = today

    if request.method == 'POST':  # 得到新的日期范围, 需要必要的检查
        date_begin = request.form.get('start')
        date_end = request.form.get('end')
    if not (date_begin <= date_end <= today):
        return redirect(url_path_dict['mssj'])

    if date_end < today:
        l_e_table, street_name_list, l_e_name_list = read_date_mssj(date_begin, date_end)  # 获取民生事件字典
        need_refresh = 0
    else:
        if session.get('num') is None:
            session['num'] = 0
        session['num'] += 1
        l_e_table, street_name_list, l_e_name_list = read_date_mssj(date_begin, date_end, session['num'])  # 获取民生事件字典
        need_refresh = 1
    l_e_name_len = len(l_e_name_list)  # 有几个民生事件?
    if session['admin']:
        return render_template('mssj_page.html',
                               street_name_list_json=json.dumps(street_name_list),
                               l_e_table_json=json.dumps(l_e_table),
                               l_e_name_list_json=json.dumps(l_e_name_list),
                               l_e_name_len_json=json.dumps(l_e_name_len),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
    if not session['admin']:
        return render_template('ordinary_mssj_page.html',
                               street_name_list_json=json.dumps(street_name_list),
                               l_e_table_json=json.dumps(l_e_table),
                               l_e_name_list_json=json.dumps(l_e_name_list),
                               l_e_name_len_json=json.dumps(l_e_name_len),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
