"""
Name : gm_sqlconn_utils.py
Author  : 写上自己的名字
Contact : 邮箱地址
Time    : 2021/3/22 15:52
Desc: 操作MYSQL数据库
"""

import pymysql
import pyodbc

# 数据库连接信息
user = "root"
password = "mysql"
# ip地址
env20 = "192.168.2.20"
env15 = "192.168.2.15"

# show环境端口
show_xcj_sql_port = 31004
show_zcj_sql_port = 31404
show_inner_sql_port = 31604
show_analysis_sql_port = 31406

# test1环境和端口
test1_zcj_sql_port = 32404
test1_xcj_sql_port = 32004
test1_inner_sql_port = 32604
test1_syh_sql_port = 32904
test1_analysis_sql_port = 32406

# test2环境端口
test2_jydn_sql_port = 34704
test2_jydw_sql_port = 34804

# 使用15服务器的sql容器
test2_zcj_sql_port = 34404
test2_xcj_sql_port = 34004
test2_inner_sql_port = 34604

# 达梦数据库



class OperateMysql(object):
    """快速连接gmsoft内部测试数据库"""

    def __init__(self, env, host):

        # 账号密码初始化
        self.user = user
        self.password = password
        self.host = host

        # 数据库连接地址初始化, 端口初始化
        if (env == 'test2' and host == 'jydn') or (env == 'test2' and host == 'jydw'):
            # test2特殊处理,军医大内和军医大外使用ip应该是192.168.2.20
            self.env = env20
            self.jydn_port = test2_jydn_sql_port
            self.jydw_port = test2_jydw_sql_port
            try:
                self.jydn_conn = pymysql.connect(host=self.env, user=self.user,
                                                 password=self.password, port=self.jydn_port, charset='utf8mb4')
                self.jydw_conn = pymysql.connect(host=self.env, user=self.user,
                                                 password=self.password, port=self.jydw_port, charset='utf8mb4')
            except TimeoutError as e:
                print('连接超时：{}'.format(e))

            print("已创建jydn数据库连接,链接信息{}:{}".format(self.host, self.jydn_port))
            print("已创建jydw数据库连接,链接信息{}:{}".format(self.host, self.jydw_port))

        elif env == 'test2':
            # test2特殊处理，ip应该是192.168.2.15
            self.env = env15
            self.zcj_port = test2_zcj_sql_port
            self.xcj_port = test2_xcj_sql_port
            self.inner_port = test2_inner_sql_port
            try:
                self.zcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.zcj_port, charset='utf8mb4')
                self.xcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.xcj_port, charset='utf8mb4')
                self.inner_conn = pymysql.connect(host=self.env, user=self.user,
                                                  password=self.password, port=self.inner_port, charset='utf8mb4')
            except TimeoutError as e:
                print('连接超时：{}'.format(e))
            print('已创建zcj数据库连接,链接信息{}:{}'.format(self.env, self.zcj_port))
            print('已创建xcj数据库连接,链接信息{}:{}'.format(self.env, self.xcj_port))
            print("已创建inner数据库连接,链接信息{}:{}".format(self.env, self.inner_port))

        elif env == 'show':
            self.env = env20
            self.xcj_port = show_xcj_sql_port
            self.zcj_port = show_zcj_sql_port
            self.inner_port = show_inner_sql_port
            self.analysis_port = show_analysis_sql_port
            try:
                self.zcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.zcj_port, charset='utf8mb4')
                self.xcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.xcj_port, charset='utf8mb4')
                self.inner_conn = pymysql.connect(host=self.env, user=self.user,
                                                  password=self.password, port=self.inner_port, charset='utf8mb4')
                self.analysis_conn = pymysql.connect(host=self.env, user=self.user,
                                                     password=self.password, port=self.analysis_port, charset='utf8mb4')
            except TimeoutError as e:
                print("连接超时：{}".format(e))
            print("已创建zcj数据库连接,链接信息{}:{}".format(self.env, self.zcj_port))
            print("已创建xcj数据库连接,链接信息{}:{}".format(self.env, self.xcj_port))
            print("已创建inner数据库连接,链接信息{}:{}".format(self.env, self.inner_port))
            print("已创建analysis数据库连接,链接信息{}:{}".format(self.env, self.analysis_port))

        elif env == 'test1':
            self.env = env20
            self.zcj_port = test1_zcj_sql_port
            self.xcj_port = test1_xcj_sql_port
            self.inner_port = test1_inner_sql_port
            self.syh_port = test1_syh_sql_port
            self.analysis_port = test1_analysis_sql_port

            try:
                self.zcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.zcj_port, charset='utf8mb4')
                self.xcj_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.xcj_port, charset='utf8mb4')
                self.inner_conn = pymysql.connect(host=self.env, user=self.user,
                                                  password=self.password, port=self.inner_port, charset='utf8mb4')
                self.syh_conn = pymysql.connect(host=self.env, user=self.user,
                                                password=self.password, port=self.syh_port, charset='utf8mb4')
                self.analysis_conn = pymysql.connect(host=self.env, user=self.user,
                                                     password=self.password, port=self.analysis_port, charset='utf8mb4')
            except TimeoutError as e:
                print("连接超时：{}".format(e))
            print("已创建zcj数据库连接,链接信息{}:{}".format(self.env, self.zcj_port))
            print("已创建xcj数据库连接,链接信息{}:{}".format(self.env, self.xcj_port))
            print("已创建内网数据库连接,链接信息{}:{}".format(self.env, self.inner_port))
            print("已创建私有化数据库连接,链接信息{}:{}".format(self.env, self.syh_port))
            print("已创建analysis数据库连接,链接信息{}:{}".format(self.env, self.analysis_port))


        else:
            print("未获取到env或host参数")

    def select_first_data(self, sql):
        """
        查询第一条数据
        """
        try:
            # 执行 sql 语句
            if self.host == 'zcj':
                self.zcj_cursor = self.zcj_conn.cursor(pymysql.cursors.DictCursor)
                self.zcj_cursor.execute(sql)
                print("当前执行sql：{}".format(sql))
                first_data = self.zcj_cursor.fetchone()
                return first_data
            elif self.host == 'xcj':
                self.xcj_cursor = self.xcj_conn.cursor(pymysql.cursors.DictCursor)
                self.xcj_cursor.execute(sql)
                first_data = self.xcj_cursor.fetchone()
                return first_data
            elif self.host == 'syh':
                self.syh_cursor = self.syh_conn.cursor(pymysql.cursors.DictCursor)
                self.syh_cursor.execute(sql)
                first_data = self.syh_cursor.fetchone()
                return first_data
            elif self.host == 'inner':
                self.inner_cursor = self.inner_conn.cursor(pymysql.cursors.DictCursor)
                self.inner_cursor.execute(sql)
                first_data = self.inner_cursor.fetchone()
                return first_data
            elif self.host == 'jydn':
                self.jydn_cursor = self.jydn_conn.cursor(pymysql.cursors.DictCursor)
                self.jydn_cursor.execute(sql)
                first_data = self.jydn_cursor.fetchone()
                return first_data
            elif self.host == 'jydw':
                self.jydw_cursor = self.jydw_conn.cursor(pymysql.cursors.DictCursor)
                self.jydw_cursor.execute(sql)
                first_data = self.jydw_cursor.fetchone()
                return first_data
            elif self.host == 'analysis':
                self.analysis_cursor = self.analysis_conn.cursor(pymysql.cursors.DictCursor)
                self.analysis_cursor.execute(sql)
                first_data = self.analysis_cursor.fetchone()
                return first_data
        except TypeError as first_data:
            print("SQL执行时类型错误！请检查：{}".format(first_data))

    def select_all_data(self, sql):
        """
        查询所有数据
        :param sql:
        :return:
        """
        try:
            # 执行 sql 语句
            if self.host == 'zcj':
                self.zcj_cursor = self.zcj_conn.cursor(pymysql.cursors.DictCursor)
                self.zcj_cursor.execute(sql)
                print("当前执行sql：{}".format(sql))
                first_data = self.zcj_cursor.fetchall()
                return first_data
            elif self.host == 'xcj':
                self.xcj_cursor = self.xcj_conn.cursor(pymysql.cursors.DictCursor)
                self.xcj_cursor.execute(sql)
                first_data = self.xcj_cursor.fetchall()
                return first_data
            elif self.host == 'syh':
                self.syh_cursor = self.syh_conn.cursor(pymysql.cursors.DictCursor)
                self.syh_cursor.execute(sql)
                first_data = self.xcj_cursor.fetchall()
                return first_data
            elif self.host == 'inner':
                self.inner_cursor = self.inner_conn.cursor(pymysql.cursors.DictCursor)
                self.inner_cursor.execute(sql)
                first_data = self.inner_cursor.fetchall()
                return first_data
            elif self.host == 'jydn':
                self.jydn_cursor = self.jydn_conn.cursor(pymysql.cursors.DictCursor)
                self.jydn_cursor.execute(sql)
                first_data = self.jydn_cursor.fetchall()
                return first_data
            elif self.host == 'jydw':
                self.jydw_cursor = self.jydw_conn.cursor(pymysql.cursors.DictCursor)
                self.jydw_cursor.execute(sql)
                first_data = self.jydw_cursor.fetchall()
                return first_data
            elif self.host == 'analysis':
                self.analysis_cursor = self.analysis_conn.cursor(pymysql.cursors.DictCursor)
                self.analysis_cursor.execute(sql)
                all_data = self.analysis_cursor.fetchone()
                return all_data
        except TypeError as first_data:
            print("SQL执行时类型错误！请检查：{}".format(first_data))

    def delete_data(self, host, sql):
        """
        查询所有数据
        :param host:  zcj、xcj
        :param sql: SQL查询
        :return:
        """
        try:
            if host == 'zcj':
                self.zcj_cursor.execute(sql)
                self.zcj_cursor.commit()
            elif host == 'xcj':
                self.xcj_cursor.execute(sql)
                self.xcj_cursor.commit()

        except TypeError as e1:
            print("SQL执行时类型错误！请检查" % e1)
            self.zcj_cursor.rollback()  # 回滚操作
            self.xcj_cursor.rollback()  # 回滚操作
        except Exception as e2:
            print("执行sql异常:%s" % e2)
            self.zcj_cursor.rollback()  # 回滚操作
            self.xcj_cursor.rollback()  # 回滚操作

    def conn_close(self):
        # 关闭数据库连接
        try:
            if hasattr(self, 'xcj_conn'):
                self.xcj_conn.close()
            if hasattr(self, 'zcj_conn'):
                self.zcj_conn.close()
            if hasattr(self, 'jydn_conn'):
                self.jydn_conn.close()
            if hasattr(self, 'jydw_conn'):
                self.jydw_conn.close()
            if hasattr(self, 'syh_conn'):
                self.syh_conn.close()
            if hasattr(self, 'inner_conn'):
                self.inner_conn.close()
            if hasattr(self, 'xcj_cursor'):
                self.xcj_cursor.close()
            if hasattr(self, 'zcj_cursor'):
                self.zcj_cursor.close()
            if hasattr(self, 'jydn_cursor'):
                self.jydn_cursor.close()
            if hasattr(self, 'jydw_cursor'):
                self.jydw_cursor.close()
            if hasattr(self, 'syh_cursor'):
                self.syh_cursor.close()
            if hasattr(self, 'inner_cursor'):
                self.inner_cursor.close()
        except AttributeError as e:
            print("数据库连接已关闭!!!")


class DMSql(object):

    def __init__(self):
        CONN_STR = (
            r'DRIVER={DM8 ODBC DRIVER};'
            r'SERVER=192.168.2.32:34994;'  # 服务器地址
            r'DATABASE=DJC_EXPERT;'  # 数据库名
            r'UID=djc_expert;'  # 用户名
            r'PWD=111111111;'  # 密码
        )
        self.conn = pyodbc.connect(CONN_STR)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        print('关闭达梦数据库连接！！！')

    def query(self, sql: str, params=None):
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"An error occurred:{e}")
            return []

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            # result = self.cursor.fetchone()
            # return result
        except Exception as e:
            print(f"An error occurred:{e}")
            return []

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            # result = self.cursor.fetchone()
            # return result
        except Exception as e:
            print(f"An error occurred:{e}")
            return []

    def count(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 1 and len(result[0]) == 1:
            # 如果结果集只有一个元素，返回那个元素
                return result[0][0]
        except Exception as e:
            print(f"An error occurred:{e}")
            return []

if __name__ == "__main__":
    # # 生成类实例对象
    # om = OperateMysql('show', 'analysis')
    # # 执行sql
    # a = om.select_all_data("SELECT count(*) FROM `datasupervision`.`zcj_contract_other_info`")
    # #
    # print(a)
    # # 关闭数据库连接l
    # om.conn_close()

    # 达梦
    with DMSql() as dm:
        # result = dm.count("SELECT count(*) FROM APPLY")
        # dm.delete(f'delete from APPLY where id = 1314547384973545472;'
        #          f'delete from APPLY_DETAIL where APPLY_ID = 1314547384973545472;'
        #          f'delete from OPERATE_RECORD where BUSINESS_ID = 1314547384973545472;')
        # s = dm.query('select s.APPLY_ID, s.APPLY_DETAIL_ID, s.EXPERT_ID, s.EXPERT_NAME, s.EXPERT_PHONE, s.CREATE_TIME from APPLY_RESULT s;')
        s = dm.query('select s.APPLY_ID, s.APPLY_DETAIL_ID, s.EXPERT_ID, s.EXPERT_NAME, s.EXPERT_PHONE, s.CREATE_TIME from APPLY_RESULT s WHERE s.id IS NOT ? LIMIT 10;', 'Null')

    print(s)
