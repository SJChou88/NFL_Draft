#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:15:06 2017

@author: stephenchou
"""

import scrapy

class RankingsSpider(scrapy.Spider):
    name = "rankings"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
        "ROBOTSTXT_OBEY":False}

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrapy shell -s 'http://collegepollarchive.com/football/ap/seasons.cfm?seasonid=2009'
#http://collegepollarchive.com/football/ap/seasons.cfm?seasonid=2009

    def start_requests(self):
        season_template_url = 'http://collegepollarchive.com/football/ap/seasons.cfm?seasonid={}'
        seasons = range(1999, 2018)
        for season in seasons:
            start_url = season_template_url.format(season)
            yield scrapy.Request(url=start_url, callback = self.getTables)

    def getTables(self, response):
        poll = response.xpath('//td[@valign="top"]//h2/text()').extract_first()
        for trow in response.xpath('//tr[@onmouseover="trfocus(this);"]'):
            try:
                rank = trow.xpath('.//strong/text()').extract_first()
                team = trow.xpath('.//a/text()').extract_first()
                tablekey = poll + " " +rank
                yield {tablekey: [poll, rank, team]}
            except:
                continue