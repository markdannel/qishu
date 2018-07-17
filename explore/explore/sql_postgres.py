#-*- coding:utf-8 -*-

import psycopg2
conn = psycopg2.connect(database="qishu", user="postgres", password="123123456", host="127.0.0.1", port="5432")
cursor = conn.cursor()
#创建 novel_name 表
# cursor.execute('DROP TABLE IF EXISTS novel_name')
cursor.execute('create table  IF NOT EXISTS novel_name(id SERIAL PRIMARY KEY, xs_name VARCHAR (255) DEFAULT NULL ,xs_author VARCHAR (255),category VARCHAR (255),name_id VARCHAR (255))')
#创建 novel_chaptername 表
# cursor.execute('DROP TABLE IF EXISTS novel_chaptername')
cursor.execute('''CREATE TABLE  IF NOT EXISTS novel_chaptername(id SERIAL PRIMARY KEY, xs_chaptername VARCHAR(255) DEFAULT NULL ,xs_content TEXT,id_name INTEGER DEFAULT NULL, 
                                                num_id INTEGER DEFAULT NULL ,url VARCHAR(255))''')
class Sql:
    #插入数据
    @classmethod
    def insert_novel_name(cls,xs_name,xs_author,category,name_id):
        # sql = "insert into novel_name (xs_name,xs_author,category,name_id) values (%(xs_name)s , %(xs_author)s , %(category)s , %(name_id)s)"
        sql = "insert into novel_name (xs_name,xs_author,category,name_id,allrank,monthrank,weekrank)" \
              " values ('%s','%s','%s','%s',0,0,0)" % (xs_name,xs_author,category,name_id)
        cursor.execute(sql)
        conn.commit()
    #查重
    @classmethod
    def select_name(cls,name_id):
        sql = "SELECT EXISTS (select 1 from novel_name where name_id = '%s')" % name_id
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()[0]


    @classmethod
    def insert_novel_chaptername(cls,xs_chaptername,xs_content,name_id,num_id,url):
        sql = '''INSERT INTO novel_chaptername(xs_chaptername , xs_content , name_id ,num_id ,
                url) VALUES ('%s' ,'%s' ,'%s' ,'%s' ,'%s')''' % (xs_chaptername,xs_content,name_id,num_id,url)
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def select_chapter(cls,url):
        sql = "SELECT EXISTS (select 1 from novel_chaptername where url = '%s')" % url
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()[0]

    @classmethod
    def insert_novel_pic(cls, summery, name_id, file_name):
        sql = '''UPDATE novel_name SET summery='%s', pic='%s'
              where name_id='%s' ''' % (summery, file_name, name_id)
        cursor.execute(sql)
        conn.commit()