from scrapy.spiders import Spider
from scrapy.selector import Selector
from bilibili.items import RankItem, UserItem
from datetime import datetime
from mysql.connector import connect
from scrapy.http import Request
from time import sleep
from scrapy_splash import SplashRequest, SplashFormRequest


def get_rank_people_url():
    my_db = connect(
        host='127.0.0.1', user='', password='', db=''
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
    if people_url is None:
        start_urls = "https://www.bilibili.com/ranking/all/0/0/30"
    else:
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

    def splash_login(self):
        login_url = 'https://passport.bilibili.com/login'
        response = Request(url=login_url)
        return SplashFormRequest.from_response(
            response,
            formdata={'mail': '', 'pass': ''},
            callback=self.parse_user()
        )

    def start_requests(self):
        script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(10))

                splash:set_viewport_full()

                local search_input = splash:select('#login-username')   
                search_input:send_text("")
                local search_input = splash:select('#login-passwd')
                search_input:send_text("")
                assert(splash:wait(5))
                local submit_button = splash:select('input[class^=primary-btn]')
                submit_button:click()

                assert(splash:wait(10))

                return {
                    html = splash:html(),
                    png = splash:png(),
                }
              end
            """
        yield SplashRequest(
            url='https://passport.bilibili.com/login',
            callback=self.after_login,  ###inserting callabck
            endpoint='execute',
            args={
                'lua_source': script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
            }
        )

    def after_login(self):
        people_url = get_rank_people_url()
        people_response = []
        cnt = 0
        for item in people_url:
            url = "https:" + item
            splash_args = {"lua_source": """
                                --splash.response_body_enabled = true
                                splash.private_mode_enabled = false
                                splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                                splash:wait(3)
                                return {html = splash:html()}
                                """}
                                         # + "\nassert(splash:go(" + url + '"))'}
            temp_response = SplashRequest(url, endpoint='run', args=splash_args, callback=self.parse_user)
            # with open('temp.html', 'w+') as f:
            #     # f.write(temp_response.text)
            people_response.append(temp_response)
            sleep(2)
            cnt += 1
            if cnt > 1:
                break
        return people_response

    def parse_user(self, response):
        # 页面提取问题，页面通过JS渲染得到，无法直接获取数据
        response = Selector(response)
        name = response.xpath('/html/head/title/text()').extract()[0].split('的')[0]
        label = response.xpath('/html/head/meta[5]/@content').extract()[0]
        des = response.xpath('/html/head/meta[6]/@content').extract()[0]
