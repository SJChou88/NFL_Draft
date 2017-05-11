#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:15:06 2017

@author: stephenchou
"""

import scrapy

class Draft(scrapy.Spider):
    name = "draft"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
        "ROBOTSTXT_OBEY":False}

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrape seasons for leagues, make list of leagues like, premier, bundesliga...
#scrapy shell 'http://www.pro-football-reference.com/years/2017/draft.htm'
#scrapy crawl combine -o combine_update.json
#start with only premier league. scrape tables for positions. premier league can just scroll through season ids.

    def start_requests(self):        
        year_url = 'http://www.pro-football-reference.com/years/{}/draft.htm'
        years = range(1999, 2018)
        for year in years:
            start_url = year_url.format(year)
            yield scrapy.Request(url=start_url, callback = self.getDraft)

    def getDraft(self, response):
        draft_year = response.xpath('//div[@id="info"]//h1/span/text()').extract_first()
        for trow in response.xpath('//div[@id="all_drafts"]//table[@id="drafts"]//tbody/tr'):
            try:
                draft_round=trow.xpath('.//th[@data-stat="draft_round"]/text()').extract_first()
                draft_pick=trow.xpath('.//td[@data-stat="draft_pick"]/text()').extract_first()
                team=trow.xpath('.//td[@data-stat="team"]/a/text()').extract_first()
                player=trow.xpath('.//td[@data-stat="player"]//a/text()').extract_first()
                pos=trow.xpath('.//td[@data-stat="pos"]/text()').extract_first()
                age=trow.xpath('.//td[@data-stat="age"]/text()').extract_first()
                college=trow.xpath('.//td[@data-stat="college_id"]/a/text()').extract_first()
                url=trow.xpath('.//td[@data-stat="college_link"]/a/@href').extract_first()
                tablekey = draft_year + " " + draft_round + " " + draft_pick
                yield {tablekey: [draft_year, draft_round,draft_pick,team,player,pos,age,college, url]}
            except:
                continue