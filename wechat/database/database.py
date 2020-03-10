# -*- coding: utf-8 -*-
"""

@Time    : 20-3-6 下午7:39
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : database.py

"""
import pymysql
from pymysql.cursors import DictCursor


class Database():
    def __init__(self):
        self.database = pymysql.connect(
            host='localhost',
            user='root',
            password='588066',
            charset='utf8',
            db='wechat'
        )
        self.cursor = self.database.cursor(DictCursor)

    def inquire(self, table, data, param, count=True):
        params = ["%s='%s'"%(k,v) for k, v in data.items() if k in param]
        sql = "select * from %s where %s" % (table, ' and '.join(params))
        # print(sql)
        self.cursor.execute(sql)
        if count is True:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()
        return result

    def insert(self, table, data):
        keys = list(data.keys())
        values = [str(data[i]) for i in keys]
        sql = "insert into %s (%s) values('%s')" % (table, ','.join(keys), "','".join(values))
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.database.commit()
        except Exception as e:
            print(e)
            print(sql)
            self.database.rollback()

    def update(self, table, data, param, field=None):
        setData = ','.join(["%s='%s'" % (k, v) for k, v in data.items() if k not in param])
        if field is not None:
            if len(field) != 0:
                setData += ',%s=NOW()' % field
            else:
                setData += '%s=NOW()' % field
        paramData = ' and '.join(["%s='%s'" % (i, data[i]) for i in param])
        sql = "UPDATE %s SET %s WHERE %s" % (table, setData, paramData)
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.database.commit()
            print('TABLE %s FINISH UPDATE' % table)
        except Exception as e:
            self.database.rollback()
            print(sql)
            print(e)

    def close(self):
        self.cursor.close()
        self.database.close()


    def main(self):
        data = {'username': 'lwh'}
        self.inquire('user', data)
        self.close()


def main():
    db = Database()
    db.main()

if __name__ == '__main__':
    main()