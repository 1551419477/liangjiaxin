# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from loguru import logger
from itemadapter import ItemAdapter
from zhnoverl.settings import LocalMysql
from zhnoverl.items import ZhnoverlItemCatalogInfo,ZhnoverlItemChatherContent,ZhnoverlItem
class ZhnoverlPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.Connection(**LocalMysql)
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):
        if isinstance(item, ZhnoverlItem):
            book_name=item['book_name']
            book_author=item['book_author']
            book_brief = item['book_brief']
            book_nums = item['book_nums']
            book_type = item['book_type']
            book_url =item['book_url']
            all_catalog = item['all_catalog']
            book=(book_name,book_author,book_brief,book_nums,book_type,book_url,all_catalog)
            sql=f"insert into book_brief(book_name,book_author,brief_introduction,book_nums,book_type,bool_url,book_catalog_url) values{book}"
            self.cur.execute(sql)
            self.conn.commit()
            logger.info(sql)
        if isinstance(item, ZhnoverlItemCatalogInfo):
            chather_title = item['chather_title']
            chather_url = item['chather_url']
            all_catalog = item['all_catalog']
            caltalog=(chather_title,chather_url,all_catalog)
            sql=f"insert into catalog_content(chather_title,chapter_url,book_catalog_url) values {caltalog}"
            self.cur.execute(sql)
            self.conn.commit()
            logger.info(sql)
        if isinstance(item, ZhnoverlItemChatherContent):
            chather_content = item['chather_content']
            chather_url = item['chather_url']
            # content=(chather_content,chather_url)
            sql=f"update catalog_content set chapter_content='{str(chather_content)}' where chapter_url='{chather_url}'"
            self.cur.execute(sql)
            # self.cur.executemany()

            self.conn.commit()
            logger.info(sql)

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


















