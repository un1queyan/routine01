import pymysql


def get_list(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def modify(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    conn.commit()
    cursor.close()
    conn.close()

def get_one(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res
def multiple_modify(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.executemany(sql, args)
    conn.commit()
    cursor.close()
    conn.close()