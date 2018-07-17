# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from explore.sql import Sql
from explore.sql import Sql
from explore.items import NovelListItem ,NovelItem, NovelpicItem
from explore import settings
import os
import urllib.request

class ExplorePipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,NovelListItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert_novel_name(xs_name,xs_author,category,name_id)
                print(u'开始存小说标题')
        if isinstance(item,NovelItem):
            url = item['chapterurl']
            name_id = item['id_name']
            num_id = item['num']
            xs_chaptername = item['chaptername']
            xs_content = item['chaptercontent']
            Sql.insert_novel_chaptername(xs_chaptername,xs_content,name_id,num_id,url)
            print(xs_chaptername, u' 存储完毕')
            return item
        if isinstance(item,NovelpicItem):
            dir_path = '%s%s'%(settings.IMAGES_STORE, 'book')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            summery = item['summery']
            name_id = item['name_id']
            picurl  = item['picurl']
            list_name = picurl.split('/')
            file_name = list_name[len(list_name) - 1]  # 图片名称
            file_path = '%s/%s' % (dir_path, file_name)
            Sql.insert_novel_pic(summery, name_id, file_name)
            if os.path.exists(file_path):
                return item
            with open(file_path, 'wb') as file_writer:
                conn = urllib.request.urlopen(picurl)  # 下载图片
                file_writer.write(conn.read())
            file_writer.close()
