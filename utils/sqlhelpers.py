
import pymysql

class SqlHelper(object):

    def connect(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()
        return res

    def get_one(self,sql,args):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchone()
        return res
    def modify(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def create(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid # 添加并且拿返回值

    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql,args)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()