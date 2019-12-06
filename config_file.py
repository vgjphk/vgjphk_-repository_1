"""
全局配置文件，配置全局变量, 要额外安装库mysql-connector-python
"""

# 根据实际情况更改字典db_parameter, 不需要更改本文件中其他部分
db_parameter = {  # 数据库参数字典
    'db_name': 'software engineering data',  # 数据库名, 该数据库中有三张表, 一张是自己导入的坪山区数据的表,
    # 另外两张是运行init_database.py就会自动生成的用户表和角色表
    'table_name': 'datas',  # 存放坪山区的数据的表的名称
    'host_name': 'localhost',  # 主机名
    'db_username': 'root',  # 数据库用户名
    'db_password': '9910250336',  # 数据库密码
    'port_number': '3306',  # 端口号
    'character_set': 'utf8mb4',  # 字符集
}
today = '2018-10-30'
yesterday = '2018-10-29'


# 配置app
def config_app(app):
    app.config['SECRET_KEY'] = 'hshs'  # 机密字符串, 随意
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+mysqlconnector://' + db_parameter['db_username'] + ':' + db_parameter['db_password'] + '@' \
        + db_parameter['host_name'] + ':' + db_parameter['port_number'] + '/' + db_parameter['db_name'] \
        + '?' + 'charset=' + db_parameter['character_set']
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'mysql+mysqlconnector://用户名:密码@localhost(这是默认的主机名):3306(端口名默认为3306)/数据库名?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
