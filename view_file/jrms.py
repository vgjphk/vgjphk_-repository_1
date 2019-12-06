from flask import render_template, session, request, redirect
from flask import Blueprint
import json
import pymysql
import pandas as pd

from config_file import today, db_parameter
from view_file.auxiliary import sort_by_col, list_to_dict, url_path_dict


def read_date_jrms(date_begin, date_end, num=0):
    '''
    :param date_begin: 起始时间
    :param date_end: 终止时间
    :param num: 若data_end为今日, 则过去的数据照常返回, 今日当天只返回num行, 若今日不足num行, 则只返回今日数据
    :return: 符合要求的数据
    '''
    if date_end < today:
        date_end += ' 23:59:59'
    elif date_end == today:
        mysql_command2 = "select 统计时间, 问题性质名称 from " + db_parameter['table_name'] + " where 统计时间>'" + today + \
                         "'and 统计时间<'" + today + " 23:59:59" + "';"
    else:
        raise Exception
    mysql_command = "select 问题性质名称 from " + db_parameter['table_name'] + " where 统计时间>'" + date_begin + \
                    "'and 统计时间<'" + date_end + "';"
    cursor = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                             password=db_parameter['db_password'],
                             db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                             charset=db_parameter['character_set'])
    problem_properties_list = list(pd.read_sql(mysql_command, con=cursor)['问题性质名称'])
    if date_end == today:
        di = pd.read_sql(mysql_command2, con=cursor)  # 读取今日数据
        tt = [list(di['统计时间']), list(di['问题性质名称'])]
        tt = sort_by_col(tt)[1][:num]
        problem_properties_list.extend(tt)

    type_name = []
    type_num = []
    problem_properties_dict = list_to_dict(problem_properties_list)
    for key in problem_properties_dict:
        type_name.append(key)
        type_num.append(problem_properties_dict[key])
    leng = len(type_name)
    return type_name, type_num, leng


jrms_blue = Blueprint('jrms_blue', __name__)  # jrms是今日民生的拼音首字母


@jrms_blue.route('/jrms/', methods=['Get', 'POST'])
def jrms_view_fun():  # 今日民生的视图函数
    if session.get('already_logged_in') != True:
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    from config_file import today
    date_begin = date_end = today

    if request.method == 'POST':  # 得到新的日期范围, 需要必要的检查
        date_begin = request.form.get('start')
        date_end = request.form.get('end')
    if not (date_begin <= date_end <= today):
        return redirect(url_path_dict['jrms'])

    if date_end < today:
        type_name, type_num, leng = read_date_jrms(date_begin, date_end)
        need_refresh = 0
    else:
        if session.get('num') == None:
            session['num'] = 0
        session['num'] += 1
        type_name, type_num, leng = read_date_jrms(date_begin, date_end, session['num'])
        need_refresh = 1
        if session['admin']:
            return render_template('jrms_page.html', type_name_json=json.dumps(type_name),
                                   type_num_json=json.dumps(type_num), leng_json=json.dumps(leng),
                                   need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面

        if not session['admin']:
            return render_template('ordinary_jrms.html', type_name_json=json.dumps(type_name),
                                   type_num_json=json.dumps(type_num), leng_json=json.dumps(leng),
                                   need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
