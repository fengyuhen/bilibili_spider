# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crwal_time = scrapy.Field()
    video_name = scrapy.Field()
    video_id = scrapy.Field()
    video_link = scrapy.Field()
    video_play_num = scrapy.Field()
    video_danmu_num = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()
    author_link = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    crwal_time = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    user_des = scrapy.Field()
    user_label = scrapy.Field()
    follow_num = scrapy.Field()
    followed_num = scrapy.Field()
    get_up_num = scrapy.Field()
    get_play_num = scrapy.Field()
    get_read_num = scrapy.Field()
    user_level = scrapy.Field()
    vip_type = scrapy.Field()


class UserRelation(scrapy.Item):
    user_id = scrapy.Field()
    relation_user_id = scrapy.Field()
    relation_type_id = scrapy.Field()