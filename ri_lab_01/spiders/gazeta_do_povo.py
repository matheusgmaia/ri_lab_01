# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from scrapy.loader import ItemLoader


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = [""]
    blacklist = ["colunistas", "blogs"]
    went_urls = [""]
    count = 0
    limit = 100

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
        
        for href in response.xpath('//article//a//@href').getall():
            if not any( blocked in href for blocked in self.blacklist):
                #Para tentar evitar alguns sites que não são artigos, como tabela de campeonato e seções do site
                if(href[-1] != "/"): 
                    if(self.count > self.limit):
                        break
                    self.went_urls.append(href)
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
        
        l = ItemLoader(item=RiLab01Item(), response=response)


        text = response.xpath('//div[@class="col-8 c-content"]//p/text()').getall()
        text = "".join(text)
        
        title = response.xpath('//h1[@class="c-title"]/text()').get()
        

        
        l.add_value('_id', title)        
        l.add_value('title', title)        
        l.add_value('sub_title', "")        
        l.add_xpath('author', "//div[@class='c-credits mobile-hide']//span")
        l.add_xpath('date', "//div[@class='c-credits mobile-hide']//li[3]")
        l.add_xpath('section', "//div[@class='c-mobile-relative']//span")
        l.add_value('text', text)
        l.add_value('url', response.url)

        self.count += 1
        return l.load_item()

#Fiz o básico, ficaram algumas duvidas, era bom um "gabarito"