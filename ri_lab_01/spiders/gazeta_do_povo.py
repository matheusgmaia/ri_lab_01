# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = [""]

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        #
        # inclua seu código aqui
        #

        # follow links to author pages
        blacklist = ["colunistas", "blogs"]
        for href in response.xpath('//article//a//@href').getall():
            if not any( blocked in href for blocked in blacklist):
                yield response.follow(href, self.parse_article)
            

        '''page = response.url.split("/")[-2]
        filename = 'news-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)'''

    def parse_article(self, response):
        self.log('Entrou em %s' % response.url)
        def extract_with_html(query):
            return response.xpath(query).get(default='')

        title = extract_with_html('//h1[@class="c-title"]/text()')
        author = extract_with_html('//div[@class="c-credits mobile-hide"]//span/text()')
        date = extract_with_html('//div[@class="c-credits mobile-hide"]//li[3]/text()')
        section = extract_with_html('//div[@class="c-mobile-relative"]//span/text()')
        text = response.xpath('//div[@class="col-8 c-content"]//p/text()').getall()
        text = "".join(text)

        item = RiLab01Item()
        item[title] = title
        item[author] = tauthoritle
        item[date] = date
        item[section] = section
        item[text] = text
        item[url] = response.url

        yield item
