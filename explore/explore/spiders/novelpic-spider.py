#-*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
import logging
# from explore.sql import Sql
from explore.sql import Sql
from explore.items import NovelListItem ,NovelItem, NovelpicItem

class novelpic_spider(scrapy.Spider):
    name = 'novelpic'
    allowed_domains = ["x23us.com"]
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]
    start_urls = [
        "http://www.x23us.com/class/1_1.html",
        "http://www.x23us.com/class/2_1.html",
        "http://www.x23us.com/class/3_1.html",
        "http://www.x23us.com/class/4_1.html",
        "http://www.x23us.com/class/5_1.html",
        "http://www.x23us.com/class/6_1.html",
        "http://www.x23us.com/class/7_1.html",
        "http://www.x23us.com/class/8_1.html",
        "http://www.x23us.com/class/9_1.html",
        "http://www.x23us.com/class/10_1.html"
    ]

    def parse(self,response):
            
        books = response.xpath('//dd/table/tr[@bgcolor="#FFFFFF"]')#/table/tbody/tr[@bgcolor="#FFFFFF"]
        print (books.extract())
        for book in books:
            name = book.xpath('.//td[1]/a[2]/text()').extract()[0]
            author = book.xpath('.//td[3]/text()').extract()[0]
            novelurl = book.xpath('.//td[1]/a[2]/@href').extract()[0]
            serialstatus = book.xpath('.//td[6]/text()').extract()[0]
            serialnumber = book.xpath('.//td[4]/text()').extract()[0]
            category = book.xpath('//dl/dt/h2/text()').re(u'(.+) - 文章列表')[0]
            jianjieurl = book.xpath('.//td[1]/a[1]/@href').extract()[0]
            novelconturl = book.xpath('.//td[1]/a[1]/@href').extract()[0]

            #print(name, author)
            item = NovelListItem()
            item['name'] =  name
            item['author'] = author
            item['novelurl'] = novelurl
            item['serialstatus'] = serialstatus
            item['serialnumber'] = serialnumber
            item['category'] = category
            item['name_id'] = jianjieurl.split('/')[-1]

            yield item
            yield scrapy.Request(novelconturl,callback = self.get_novelcont,meta = {'name_id' : item['name_id'], 'novelconturl' : novelconturl})


    def get_novelcont(self,response):
        summery = response.xpath('//dl[@id="content"]/dd[3]/p[1]/text()')
        summery2 = response.xpath('//dl[@id="content"]')
        item = NovelpicItem()
        item['summery'] = summery2.xpath('.//dd[2]/p[2]/text()').extract()[0]
        item['name_id'] = response.meta['name_id']
        item['picurl']  = '%s%s' % ("http://www.x23us.com", summery2.xpath('.//dd[2]/div[1]/a/img/@src').extract()[0])
        yield item

    #获取章节名
    def get_chapter(self,response):
        num = 0
        allurls = response.xpath('//tr')
        for trurls in allurls:
            tdurls = trurls.xpath('.//td[@class="L"]')
            for url in tdurls:
                num = num + 1
                chapterurl = response.url + url.xpath('.//a/@href').extract()[0]
                chaptername = url.xpath('.//a/text()').extract()[0]
                rets = Sql.select_chapter(chapterurl)
                if rets[0] == 1:
                    print(u'章节已经存在了')
                    pass
                else:
                    yield scrapy.Request(url = chapterurl,callback = self.get_chaptercontent,meta={'num':num,
                                                                                               'name_id':response.meta['name_id'],
                                                                                               'chaptername':chaptername,
                                                                                               'chapterurl':chapterurl})
    #获取章节内容
    def get_chaptercontent(self,response):
        item = NovelItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = response.meta['chaptername']
        item['chapterurl'] = response.meta['chapterurl']
        content = response.xpath('//dd[@id="contents"]/text()').extract()
        item['chaptercontent'] = '\n   '.join(content)
        return item