from flask import render_template, session, request, redirect
from flask import Blueprint
import json
import pymysql
import pandas as pd

from config_file import today, db_parameter
from view_file.auxiliary import url_path_dict, sort_by_col


def read_date_sjjb(date_begin, date_end, num=0):
    '''
    :param date_begin: 起始时间
    :param date_end: 终止时间
    :param num: 若data_end为今日, 则过去的数据照常返回, 今日当天只返回num行, 若今日不足num行, 则只返回今日数据
    :return: 符合要求的数据
    '''
    if date_end < today:
        date_end += ' 23:59:59'
    elif date_end == today:
        mysql_command2 = "select 统计时间, 问题类型, 超期办结, 处置中, 按期办结 from " + db_parameter['table_name'] + " where 统计时间>'" + \
                         today + "'and 统计时间<'" + today + " 23:59:59" + "';"
    else:
        raise Exception
    mysql_command = "select 问题类型, 超期办结, 处置中, 按期办结 from " + db_parameter['table_name'] + " where 统计时间>'" + \
                    date_begin + "'and 统计时间<'" + date_end + "';"
    cursor = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                             password=db_parameter['db_password'],
                             db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                             charset=db_parameter['character_set'])
    di = pd.read_sql(mysql_command, con=cursor)
    dd_sjjb = [list(di['问题类型']), list(di['超期办结']), list(di['处置中']), list(di['按期办结'])]
    if date_end == today:
        di = pd.read_sql(mysql_command2, con=cursor)  # 读取今日数据
        tt = sort_by_col([list(di['统计时间']), list(di['问题类型']), list(di['超期办结']), list(di['处置中']), list(di['按期办结'])])
        dd_sjjb[0].extend(tt[1][:num])
        dd_sjjb[1].extend(tt[2][:num])
        dd_sjjb[2].extend(tt[3][:num])
        dd_sjjb[3].extend(tt[4][:num])
    temp = []
    for i in range(len(dd_sjjb[0])):
        if dd_sjjb[1][i] == '1':
            temp.append('超期办结')
        elif dd_sjjb[2][i] == '1':
            temp.append('处置中')
        elif dd_sjjb[3][i] == '1':
            temp.append('按期办结')
        else:
            temp.append('未知')
    dd_sjjb = [dd_sjjb[0], temp]

    datas_a = [];
    datas_b = [];
    datas_c = [];
    datas_d = []
    datas_a_value = [];
    datas_b_value = [];
    datas_c_value = [];
    datas_d_value = []
    datas2 = ['超期办结', '处置中', '按期办结', '未知']
    datas2_value = [0, 0, 0, 0]
    for i in range(len(dd_sjjb[0])):
        if dd_sjjb[1][i] == '超期办结':
            datas2_value[0] += 1
            if dd_sjjb[0][i] not in datas_a:  # 若这个问题类型还没有被收录
                datas_a.append(dd_sjjb[0][i])
                datas_a_value.append(1)
            else:  # 若这个问题类型已经被收录
                index = datas_a.index(dd_sjjb[0][i])
                datas_a_value[index] += 1
        elif dd_sjjb[1][i] == '处置中':
            datas2_value[1] += 1
            if dd_sjjb[0][i] not in datas_b:  # 若这个问题类型还没有被收录
                datas_b.append(dd_sjjb[0][i])
                datas_b_value.append(1)
            else:  # 若这个问题类型已经被收录
                index = datas_b.index(dd_sjjb[0][i])
                datas_b_value[index] += 1
        elif dd_sjjb[1][i] == '按期办结':
            datas2_value[2] += 1
            if dd_sjjb[0][i] not in datas_c:  # 若这个问题类型还没有被收录
                datas_c.append(dd_sjjb[0][i])
                datas_c_value.append(1)
            else:  # 若这个问题类型已经被收录
                index = datas_c.index(dd_sjjb[0][i])
                datas_c_value[index] += 1
        elif dd_sjjb[1][i] == '未知':
            datas2_value[3] += 1
            if dd_sjjb[0][i] not in datas_d:  # 若这个问题类型还没有被收录
                datas_d.append(dd_sjjb[0][i])
                datas_d_value.append(1)
            else:  # 若这个问题类型已经被收录
                index = datas_d.index(dd_sjjb[0][i])
                datas_d_value[index] += 1

    datas = []
    datas_value = []
    for datas_x, datas_x_value, t1 in zip([datas_a, datas_b, datas_c, datas_d],
                                          [datas_a_value, datas_b_value, datas_c_value, datas_d_value],
                                          ['超期办结', '处置中', '按期办结', '未知']):
        if datas_x == []:
            datas2.remove(t1)
            datas2_value.remove(0)
        else:
            datas.extend(datas_x)
            datas_value.extend(datas_x_value)

    return datas, datas_value, datas2, datas2_value


sjjb_blue = Blueprint('sjjb_blue', __name__)  # sjjb是事件结办的拼音首字母


@sjjb_blue.route('/sjjb/', methods=['Get', 'POST'])
def sjjb_view_fun():  # 事件结办分析的视图函数
    if session.get('already_logged_in') != True:
        return redirect(url_path_dict['login'])  # 未登录, 重定向到登陆页面
    from config_file import today
    date_begin = date_end = today

    if request.method == 'POST':  # 得到新的日期范围, 需要必要的检查
        date_begin = request.form.get('start')
        date_end = request.form.get('end')
    if not (date_begin <= date_end <= today):
        return redirect(url_path_dict['sjjb'])

    if date_end < today:
        datas, datas_value, datas2, datas2_value = read_date_sjjb(date_begin, date_end)  # 获取事件结办
        need_refresh = 0
    else:
        if session.get('num') == None:
            session['num'] = 0
        session['num'] = session['num'] + 1
        datas, datas_value, datas2, datas2_value = read_date_sjjb(date_begin, date_end, session['num'])  # 获取事件结办
        need_refresh = 1

    # 若全是空表, 传到前端, 则不显示图表
    if session['admin']:
        return render_template('sjjb_page.html', datas_json=json.dumps(datas), datas_value_json=json.dumps(datas_value),
                               datas2_json=json.dumps(datas2), datas2_value_json=json.dumps(datas2_value),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
    if not session['admin']:
        return render_template('ordinary_sjjb_page.html', datas_json=json.dumps(datas), datas_value_json=json.dumps(datas_value),
                               datas2_json=json.dumps(datas2), datas2_value_json=json.dumps(datas2_value),
                               need_refresh=need_refresh)  # 从后端传到前端, 用对象渲染页面后返回该页面
