# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from mysql.connector import connect


class BilibiliPipeline:
    def process_item(self, item, spider):
        mydb = connect(
            host='', user='', password='', db='bilibili_spider'
        )
        sql_insert_1 = '''INSERT INTO rank (crwal_time, video_name, video_link, video_play_num, video_danmu_num, video_id, author_name, author_link, author_id) VALUES ('''
        sql_insert_2 = self.to_sql_str(item['crwal_time']) + ',' + self.to_sql_str(item['video_name'])\
                       + ',' + self.to_sql_str(item['video_link']) + ',' \
                       + str(item['video_play_num']) + ',' + str(item['video_danmu_num']) + ',' \
                       + self.to_sql_str(item['video_id']) + ',' + self.to_sql_str(item['author_name'])\
                       + ',' + self.to_sql_str(item['author_link']) + ',' + self.to_sql_str(item['author_id']) + ');'
        sql = sql_insert_1 + sql_insert_2
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql)
            mydb.commit()
        except:
            print('sql_error')
        return item

    @staticmethod
    def to_sql_str(str):
        return '"' + str + '"'
