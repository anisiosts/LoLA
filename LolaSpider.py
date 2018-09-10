# -*- coding: utf-8 -*-
import scrapy

class LolaSpider(scrapy.Spider):
    name = 'LolaSpider'
    allowed_domains = ['na.leagueoflegends.com']
    start_urls = ['https://na.leagueoflegends.com/en/tag/patch-notes']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        urls = response.css('div.default-2-3 > h4 > a::attr(href)').extract()

        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_patch)
        
        next_page = response.css('div.pager > a.next::attr(href)').extract_first()
        if next_page:
            self.log('ENTROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOCARAI')
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_patch(self, response):
        self.log('I just visited: ' + response.url)
        for block in response.css('div.patch-change-block'):
            champ = {
                'Link' : response.url,
                'Patch' : response.css('h1.article-title::text').extract_first(),
                'Nome' : block.css('h3 > a::text').extract_first(),
                'Sumario' : block.css('p.summary::text').extract_first(),
                'Texto' : block.css('blockquote::text').extract_first(),
                'Skills' : block.css('h4::text').extract(),
            }
            yield champ
