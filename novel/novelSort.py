# 导入redis，进行建立连接，直接操作redis,而不是cache
# from redis import Redis
from redis import Redis
from .models import Name
import hashlib
# id : { 'name':name, 'type': type, 'cnum': clicknum}
# 需求先启动redis服务器
r = Redis(host='127.0.0.1',port=6379, decode_responses=True)

def content_click(book_id, category,count=1):
    str = category
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    r.zincrby(hl.hexdigest(),book_id,count)

def all_click(book_id, count=1):
    r.zincrby('Book-clicks', book_id,count)

# 获取排行前num位的数据
def get_top_n_books(num):
    #zrevrange key start stop [WITHSCORES]  
    #返回有序集 key 中，指定区间内的成员
    article_clicks=r.zrevrange('Book-clicks',0,num,withscores=True)
    print("0-10 -> ", article_clicks)
    #返回前num项数据，每一包含（'Article-clicks',article_id,count）
    #取出id和count
    articles = Name.objects.in_bulk([item[0] for item in article_clicks]) 
    #根据列表中的所有id,一次取出所有的文章
    
    return articles, article_clicks