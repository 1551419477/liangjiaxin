import scrapy
from loguru import logger
from zhnoverl.items import ZhnoverlItem,ZhnoverlItemCatalogInfo,ZhnoverlItemChatherContent
class ZhSpider(scrapy.Spider):
    name = 'zh'
    start_urls = ['http://book.zongheng.com/store/c0/c0/b0/u0/p1/v0/s1/t0/u0/i1/ALL.html']

    def parse(self, response):

        logger.info(response.url)
        book_url_list=response.xpath('//div[@class="bookname"]/a/@href').extract()
        # logger.info(len(book_url_list))
        # logger.info(type(book_url_list))
        for book_url in book_url_list:
            yield scrapy.Request(book_url,callback=self.parse_book_info)

    def parse_book_info(self,response):
        book_name=response.xpath('//div[@class="book-name"]/text()').extract()[0].strip()
        book_author=response.xpath('//div[@class="au-name"]/a/text()').extract()[0].strip()

        book_nums=response.xpath('//div[@class="nums"]/span/i/text()').extract()[0].strip()

        book_type = response.xpath('//div[@class="crumb"]/a/text()').extract()[1].strip()
        book_brief = response.xpath('//div[@class="book-dec Jbook-dec hide"]/p/text()').extract()
        book_brief="".join(book_brief)
        all_catalog = response.xpath('//a[@class="all-catalog"]/@href').extract()[0]

        item=ZhnoverlItem()
        item['book_name']=book_name
        item['book_author']=book_author
        item['book_nums']=book_nums
        item['book_type']=book_type
        item['book_url']=response.url
        item['all_catalog']=all_catalog
        item['book_brief']=book_brief

        yield item
        yield scrapy.Request(all_catalog,callback=self.parse_catalog_info)


    def parse_catalog_info(self,response):
        logger.info(response.url)
        lis=response.xpath('//ul[@class="chapter-list clearfix"]//li')
        item=ZhnoverlItemCatalogInfo()
        for li in lis[0:10]:
            chather_title=li.xpath('.//a/text()').extract()[0]
            chather_url=li.xpath('.//a/@href').extract()[0]
            item['chather_title']=chather_title
            item['chather_url']=chather_url
            item['all_catalog']=response.url
            yield item
            yield scrapy.Request(chather_url,callback=self.parse_chapter_content)


    def parse_chapter_content(self,response):
        item=ZhnoverlItemChatherContent()
        ps = response.xpath('//div[@class="content"]/p')
        p_list = []
        for p in ps:
            content = p.xpath('./text()').getall()[0].strip()
            p_list.append(content)
        text = "".join(p_list)

        item['chather_content']=text
        item['chather_url']=response.url
        yield item
        pass




