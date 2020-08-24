from scrapy.spiders import Spider
from bilibili.items import RankItem
from datetime import datetime
from mysql.connector import connect


def get_rank_people_url():
    my_db = connect(
        host='127.0.0.1', user='spider', password='Spider123...', db='bilibili_spider'
    )
    sql = "select `rank`.author_link link from rank;"
    try:
        my_cursor = my_db.cursor()
        my_cursor.execute(sql)
        result = my_cursor.fetchall()
        result = [item[0] for item in result]
        return result
    except:
        print("get rank people link error from MySQL db")
        return None


class BilibiliSpider(Spider):
    name = "b_spider"
    allowed_domains = ["bilibili.com"]
    people_url = get_rank_people_url()
    if people_url is not None:
        pass
    else:
        start_urls = "https://www.bilibili.com/ranking/all/0/0/30"
    people_url = get_rank_people_url()


    def parse(self, response, **kwargs):
        ranks = response.css('#app > div.b-page-body > div > div.rank-container > div.rank-body > div.rank-list-wrap >'
                             ' ul > li')
        ranks_30_video_info = []
        for rank in ranks:
            item = RankItem()
            item['crwal_time'] = datetime.now().strftime('%Y-%m-%d')
            item['video_name'] = rank.css('div.content > div.info > a::text').extract()[0]
            item['video_link'] = rank.css('div.content > div.info > a ::attr(href)').extract()[0]
            item['video_play_num'] = rank.css('div.content > div.info > div.detail > span.data-box ::text').extract()[0]
            item['video_danmu_num'] = rank.css('div.content > div.info > div.detail > span.data-box'
                                               ' ::text').extract()[1]
            item['video_id'] = item['video_link'].split('/')[-1]
            item['author_name'] = rank.css('div.content > div.info > div.detail > a ::text').extract()[0]
            item['author_link'] = rank.css('div.content > div.info > div.detail > a ::attr(href)').extract()[0]
            item['author_id'] = item['author_link'].split('/')[-1]

            if item['video_danmu_num'][-1] == '万':
                item['video_danmu_num'] = float(item['video_danmu_num'][:-1]) * 10000
                item['video_danmu_num'] = int(item['video_danmu_num'])
            if item['video_play_num'][-1] == '万':
                item['video_play_num'] = float(item['video_play_num'][:-1]) * 10000
                item['video_play_num'] = int(item['video_play_num'])

            ranks_30_video_info.append(item)

        return ranks_30_video_info

