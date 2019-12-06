def init_database():
    '''
    若数据库还未初始化, 则初始化数据库, 数据库中应人为保证没有名为roles和users的表, 才能完成初始化
    若数据库已经初始化, 则什么都不会发生
    '''
    from manage import db
    db.reflect()
    all_table = {table_obj.name: table_obj for table_obj in db.get_tables_for_bind()}
    try:
        str(all_table['roles'])
        str(all_table['users'])
    except KeyError:
        from db_models.user_model import User
        from db_models.role_model import Role
        db.drop_all()
        db.create_all()
        role1 = Role(name='admin')
        role2 = Role(name='ordinary_user')
        db.session.add_all([role1, role2])
        db.session.commit()
        user1 = User(name='hshs', password='ooo', role_id=role1.id)
        user2 = User(name='hkhk', password='iii', role_id=role1.id)
        user3 = User(name='郑某人', password='me', role_id=role2.id)
        user4 = User(name='王维', password='wang', role_id=role2.id)
        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()
        print('新建了roles和users表')
    else:
        print('已存在roles和users表')


if __name__ == '__main__':
    init_database()
