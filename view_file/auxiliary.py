import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from flask import make_response, session, Blueprint
import pymysql
import pandas as pd
from sqlalchemy import create_engine

from config_file import db_parameter

local_host = 'http://127.0.0.1:5000/'
url_path_dict = {
    '': local_host + '',
    'login': local_host + 'login',
    'home': local_host + 'home',
    'register': local_host + 'register',
    'jrms': local_host + 'jrms',
    'mssj': local_host + 'mssj',
    'rdsq': local_host + 'rdsq',
    'sjjb': local_host + 'sjjb'
}

'''
session['already_logged_in'] = True/False   是否已经登陆
session['username']                         用户名字符串
session['validate_strs']                    验证码字符串
session['admin'] = True/False               是否是管理员
session['num']                              读取今日及未来的数据的数量
'''


def get_chars_str():
    '''
    :return:验证码字符集合
    '''
    _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
    return init_chars


def create_validate_code(size=(120, 30),
                         chars=get_chars_str(),
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(0, 0, 255),
                         font_size=18,

                         # 微软雅旗黑字体, 该ttf文件要和本模块同目录, 注意由于本模块是被导入的,
                         # 所以资源文件应该是在PPPPPP下的, 现放在static里, 要用相对路径
                         font_type="static/MicrosoftYaqiHeiBold-2.ttf",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=2):
    """
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    """

    width, height = size  # 宽高
    # 创建图形
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs


auxiliary_blue = Blueprint('auxiliary_blue', __name__)


@auxiliary_blue.route('/code/')
def get_code():
    validate_img, validate_strs = create_validate_code()  # 获取随机生成的验证码图片和对应的验证码字符串

    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    validate_img.save(buf, 'jpeg')
    buf_str = buf.getvalue()  # buf_str是图片的二进制形式

    # 把buf_str作为response发回前端(即浏览器)，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'

    # 将验证码字符串储存在session中
    session['validate_strs'] = validate_strs

    return response


def is_in_table_users(name):
    from db_models.user_model import User
    a_user = User.query.filter(User.name == name).all()
    if a_user != []:
        return True
    else:
        return False


def add_to_table_users(name, password):
    from manage import db
    from db_models.user_model import User
    from db_models.role_model import Role
    a_role = Role.query.filter(Role.id == 2).first()
    a_user = User(name=name, password=password, role_id=a_role.id)
    db.session.add(a_user)
    db.session.commit()


def is_admin(name):
    from db_models.user_model import User
    from db_models.role_model import Role  # 本行不可以删掉!!!!!!!!!!
    a_user = User.query.filter(User.name == name).first()
    return True if a_user.rolelalala.id == 1 else False


def read_table_columns(table_name, *columns, all_column=False):
    """
    作用: 读取数据库中的一张指定表的指定列的数据
    :param table_name: 表名
    :param columns: 若干列名
    :param all_column: 若为Ture, 则忽略columns, 并且读取整张表
    :return: 列表, 每一个元素为一个列表(代表一个指定列); 若失败则打印提示信息并返回[]
    """
    cursor = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                             password=db_parameter['db_password'],
                             db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                             charset=db_parameter['character_set'])
    cols = []
    if all_column:  # 若要整张表, 则columns是所有列名的集合
        columns = tuple(pd.read_sql('select * from ' + table_name, con=cursor))

    for i in columns:
        try:
            a_col_list = list((pd.read_sql('select ' + i + ' from ' + table_name, con=cursor))[i])
            cols.append(a_col_list)
        except:
            print('输入的列名', i, '不正确')
            cols = []
            break
    return cols


def list_to_dict(a_list):
    '''
    :param a_list: 一个列表, 如['a', 'a', 'a', 'b', 'b', 'a']
    :return: 一个字典, 该字典是列表转换而成, 比如上面的列表会转换成: {'a':4, 'b':2}, 表示'a'出现4次, 'b'出现2次
    '''
    a_dict = {}
    for i in a_list:
        try:
            a_dict[i] += 1
        except:
            a_dict[i] = 1
    return a_dict


def sort_by_col(a_sequence, order_by=0, desc=False):
    '''
    作用: 对数据进行排序
    :param a_sequence: 数据集, 是一个序列. 这个序列的每个元素都是一个序列, 代表一列数据. 要求每一列数据的长度相等
    :param order_by: 按照第几列数据进行排序, 默认是第一列
    :param desc: 若为Ture, 则按降序排列; 若为False, 则按升序排列
    :return: 排序后的数据
    '''
    # 保证 a_sequence 是一个符合要求的序列
    try:
        a_sequence + ''
    except TypeError:
        pass
    else:
        print('a_sequence是一个字符串, 请修改代码')
        raise TypeError
    try:
        a_sequence[order_by]
    except TypeError:
        print('a_sequence不是一个序列或order_by不是一个索引, 请修改代码')
        raise
    except IndexError:
        print('order_by超出索引, 请修改代码')
        raise
    for i in a_sequence:
        assert len(i) == len(a_sequence[0])

    # 排序
    try:
        def turn(m, temp):
            n = m.copy()
            for i in range(len(m)):
                n[temp[i]] = m[i]
            return n

        a_col = sorted(a_sequence[order_by]) if desc == False else sorted(a_sequence[order_by], reverse=True)
        temp = []
        for i in a_sequence[order_by]:
            for j in range(len(a_col)):
                if i == a_col[j] and (j not in temp):
                    temp.append(j)
                    break
        for i in range(len(a_sequence)):
            a_sequence[i] = turn(a_sequence[i], temp)
    except:
        print('某一列中的数据类型不一致或其他原因, 请修改代码')
        raise TypeError
    return a_sequence


def event_search(date, way, community, street, nature):
    """
    统计时间 2
    所属区域 3
    所属街道 5
    所属社区 7
    问题类型 9
    大类名称 11
    小类名称 13
    处置部门 15
    问题来源 17
    超期办结 20
    处置中 21
    按期办结 22
    问题性质名称 24
    """
    stuffs = read_table_columns(db_parameter['table_name'], all_column=True)
    target_event = {}
    for i in range(len(stuffs[0])):
        if stuffs[2][i][:10] == date and stuffs[17][i] == way and stuffs[7][i] == community and stuffs[5][
            i] == street and stuffs[24][i] == nature:
            if i not in target_event:
                target_event[i] = []
            target_event[i].append(stuffs[2][i])
            target_event[i].append(stuffs[3][i])
            target_event[i].append(stuffs[5][i])
            target_event[i].append(stuffs[7][i])
            target_event[i].append(stuffs[9][i])
            target_event[i].append(stuffs[11][i])
            target_event[i].append(stuffs[13][i])
            target_event[i].append(stuffs[15][i])
            target_event[i].append(stuffs[17][i])
            target_event[i].append(stuffs[24][i])
            if stuffs[20][i] == '1':
                target_event[i].append('超期办结')
            if stuffs[22][i] == '1':
                target_event[i].append('按期办结')
            if stuffs[21][i] == '1':
                target_event[i].append('处置中')
    return target_event


# 名称与名称对应数字标识的字典，因大类名称、小类名称和处置部门种类繁多，目前还未加入完善
message_parameter = {
    '区域': {'坪山区': '1'},
    '街道': {'碧岭街道': '100', '龙田街道': '101', '马峦街道': '102', '石井街道': '103', '坪山街道': '104', '坑梓街道': '105', },
    '社区': {'马峦社区': '10000', '金龟社区': '10001', '汤坑社区': '10002', '江岭社区': '10003', '坪环社区': '10004', '坪山社区': '10005',
           '沙坣社区': '10006', '六联社区': '10007', '田头社区': '10008', '碧岭社区': '10009', '沙湖社区': '10010', '田心社区': '10011',
           '六和社区': '10012', '竹坑社区': '10013', '老坑社区': '10014', '坑梓社区': '100015', '和平社区': '10016', '石井社区': '10017',
           '南布社区': '10018', '金沙社区': '10019', '龙田社区': '10020', '沙田社区': '10021', '秀新社区': '10022'},
    '问题类型': {'安全隐患': '1', '治安维稳': '2', '环保水务': '3', '规土城建': '4', '市容环卫': '5', '市政设施': '6', '交通运输': '7', '劳动社保': '8',
             '食药市监': '9', '文体旅游': '10', '教育卫生': '11', '组织人事': '12', '党建群团': '13', '党纪政纪': '14', '民政服务': '15',
             '统一战线': '16', '社区管理': '17', '专业事件采集': '695'},
    # '大类':{'坪山区': '1'},
    # '小类':{'坪山区': '1'},
    # '处置部门':{'坪山区': '1'},
    '问题来源': {'美丽深圳': '102', '@坪山': '103', '政府信箱': '104', '固话投诉': '106', '12319': '12', '12345': '13'},
    '问题性质': {'求决': '1', '投诉': '2', '咨询': '3', '建议': '4', '-': '99'}
}


# 将管理员手动输入的数据加入数据库末尾，目前测试无bug
def write_to_db(num, date, area, street, community, types, big_type, tiny_type, department, way, progress, nature):
    cursor = create_engine(
        'mysql+mysqlconnector://' + db_parameter['db_username'] + ':' + db_parameter['db_password'] + '@' +
        db_parameter['host_name'] + ':' + db_parameter['port_number'] + '/' + db_parameter[
            'db_name'] + '?' + 'charset=' + db_parameter['character_set'])
    con = cursor.connect()
    report_num = acceptances = '1'
    progress_list = {'超期办结': [], '处置中': [], '按期办结': []}
    if progress == '超期办结':
        progress_list['超期办结'].append('1')
        progress_list['处置中'].append('0')
        progress_list['按期办结'].append('0')
    if progress == '处置中':
        progress_list['超期办结'].append('0')
        progress_list['处置中'].append('1')
        progress_list['按期办结'].append('0')
    if progress == '按期办结':
        progress_list['超期办结'].append('0')
        progress_list['处置中'].append('0')
        progress_list['按期办结'].append('1')
    df = pd.DataFrame({'主键': [num, ],
                       '上报': [report_num, ],
                       '统计时间': [date, ],
                       '所属区域': [area, ],
                       '区域标识': [message_parameter['区域'][area], ],
                       '所属街道': [street, ],
                       '街道标识': [message_parameter['街道'][street], ],
                       '所属社区': [community, ],
                       '社区标识': [message_parameter['社区'][community], ],
                       '问题类型': [types, ],
                       '问题类型标识': [message_parameter['问题类型'][types], ],
                       '大类名称': [big_type, ],
                       '大类标识': ['-', ],
                       '小类名称': [tiny_type, ],
                       '小类标识': ['-', ],
                       '处置部门': [department, ],
                       '处置部门标识': ['-', ],
                       '问题来源': [way, ],
                       '问题来源标识': [message_parameter['问题来源'][way], ],
                       '受理': [acceptances, ],
                       '超期办结': progress_list['超期办结'][0],
                       '处置中': [progress_list['处置中'][0], ],
                       '按期办结': [progress_list['按期办结'][0], ],
                       '问题性质标识': [message_parameter['问题性质'][nature], ],
                       '问题性质名称': [nature, ]
                       })
    df.to_sql(name=db_parameter['table_name'], con=con, index=False, if_exists='append')


def if_exist(date, area, street, community, types, big_type, tiny_type, way, nature):  # 判断输入的数据是否已存在
    stuffs = read_table_columns(db_parameter['table_name'], all_column=True)
    for i in range(len(stuffs[0])):
        if stuffs[2][i][:10] == date and stuffs[17][i] == way and stuffs[7][i] == community and stuffs[5][
            i] == street and stuffs[24][i] == nature and stuffs[3][i] == area and stuffs[9][i] == types and stuffs[11][
            i] == big_type and stuffs[13][i] == tiny_type:
            return True
    return False


def search_by_num(num):
    stuffs = read_table_columns(db_parameter['table_name'], all_column=True)
    target = []
    for i in range(len(stuffs[0])):
        if stuffs[0][i] == num:
            for p in range(len(stuffs)):
                target.append(stuffs[p][i])
            break
    return target


def change_progress(target, progress):
    connect = pymysql.connect(host=db_parameter['host_name'], user=db_parameter['db_username'],
                              password=db_parameter['db_password'],
                              db=db_parameter['db_name'], port=int(db_parameter['port_number']),
                              charset=db_parameter['character_set'])

    cursor = connect.cursor()
    cursor.execute("UPDATE " + db_parameter['table_name'] + " SET 处置中 = 0 WHERE 主键 = '%s'" % (target[0]))
    connect.commit()
    cursor.execute("UPDATE " + db_parameter['table_name'] + " SET " + progress + " = 1 WHERE 主键 = '%s'" % (target[0]))
    connect.commit()
    connect.close()
