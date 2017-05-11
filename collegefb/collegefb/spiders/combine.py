#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:15:06 2017

@author: stephenchou
"""

import scrapy

class Combine(scrapy.Spider):
    name = "combine"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
        "ROBOTSTXT_OBEY":False}

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrape seasons for leagues, make list of leagues like, premier, bundesliga...
#scrapy shell 'http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min=2017&year_max=2017&height_min=65&height_max=82&weight_min=149&weight_max=375&pos=QB&pos=WR&pos=TE&pos=RB&pos=FB&pos=OT&pos=OG&pos=C&pos=DE&pos=DT&pos=ILB&pos=OLB&pos=SS&pos=FS&pos=CB&pos=LS&pos=K&pos=P&show=all&order_by=year_id'

#start with only premier league. scrape tables for positions. premier league can just scroll through season ids.

    def start_requests(self):
        pos_list = ('QB','RB','WR','TE','FB','OT','OG','C','DE','DT','ILB','OLB','SS','FS','CB','LS','K','P')
        
        year_url = 'http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={}&year_max={}&height_min=65&height_max=82&weight_min=149&weight_max=375&'
        pos_url = 'pos={}&show=all&order_by=year_id'
        years = range(2000, 2018)
        for year in years:
            for pos in pos_list:
                start_url = year_url.format(year,year)+pos_url.format(pos)
                yield scrapy.Request(url=start_url, callback = self.getCombineStats)

    def getCombineStats(self, response):
        for trow in response.xpath('//div[@id="all_results"]//tbody/tr'):
            try:
                year=trow.xpath('.//td[@data-stat="year"]/a/text()').extract_first()
                player=trow.xpath('.//td[@data-stat="player"]//a/text()').extract_first()
#                player=trow.xpath('.//td[@data-stat="player"]/text()').extract_first() for 2017
                pos=trow.xpath('.//td[@data-stat="pos"]/text()').extract_first()
                college=trow.xpath('.//td[@data-stat="school_name"]/a/text()').extract_first()
                height=trow.xpath('.//td[@data-stat="height"]/text()').extract_first()
                weight=trow.xpath('.//td[@data-stat="weight"]/text()').extract_first()
                forty=trow.xpath('.//td[@data-stat="forty_yd"]/text()').extract_first()
                vertical=trow.xpath('.//td[@data-stat="vertical"]/text()').extract_first()
                bench=trow.xpath('.//td[@data-stat="bench_reps"]/text()').extract_first()
                broad=trow.xpath('.//td[@data-stat="broad_jump"]/text()').extract_first()
                threecone=trow.xpath('.//td[@data-stat="cone"]/text()').extract_first()
                shuttle=trow.xpath('.//td[@data-stat="shuttle"]/text()').extract_first()
                drafted=trow.xpath('.//td[@data-stat="draft_info"]/text()').extract_first()
                url=trow.xpath('.//td[@data-stat="college"]/a/@href').extract_first()
                tablekey = year + " " + player + " " + pos
                yield {tablekey: [year, player, pos, college, height, weight, forty, vertical, bench, broad, threecone, shuttle, drafted, url]}
            except:
                continue