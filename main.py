from scrapy import cmdline

a = cmdline.execute('scrapy crawl b_spider -o output.json'.split())