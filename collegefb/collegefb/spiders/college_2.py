#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:15:06 2017

@author: stephenchou
"""

import scrapy

class college_2(scrapy.Spider):
    name = "college_2"
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
        for trow in response.xpath('//div[@id="all_drafts"]//table[@id="drafts"]//tbody/tr'):
            try:
                player_url=trow.xpath('.//td[@data-stat="college_link"]/a/@href').extract_first()
                yield scrapy.Request(url=player_url, callback=self.getCollegeStats)
            except:
                continue

    def getCollegeStats(self, response):
        player_url = response.url
        player_name = response.xpath('//div[@class="players"]//h1[@itemprop="name"]/text()').extract_first()
#        passing = response.xpath('//div[@id="all_passing"]//tbody')
#        rushnrec = response.xpath('//div[@id="all_rushing"]//tbody')
#        recnrush = response.xpath('//div[@id="all_receiving"]//tbody')
#        defense = response.xpath('//div[@id="all_defense"]//tbody')

        recs = 0
        rec_yds = 0
        rec_td = 0
        rush_att = 0
        rush_yds = 0
        rush_td = 0
        attempts = 0
        completions=0
        pass_ints=0
        pass_tds=0
        pass_yds = 0
        games = 0
        solo_tackles=0
        ast_tackles=0
        tackles=0
        loss_tackles=0
        sacks=0
        ints=0
        ints_tds=0
        ints_yds=0
        pds=0
        fum_rec=0
        fum_forced=0
        fum_tds=0
        fum_yds=0
        games_rush=0
        games_pass=0
        games_rec=0
        games_d=0
        for trow in response.xpath('//div[@id="all_rushing"]//tbody//tr'):
            try:
                season = trow.path('.//th[@data-stat="year_id"]/a/text()').extract_first()
                games_rush = trow.xpath('.//td[@data-stat="g"]/text()').extract_first()
                recs = trow.xpath('.//td[@data-stat="rec"]/text()').extract_first()
                rec_yds = trow.xpath('.//td[@data-stat="rec_yds"]/text()').extract_first()
                rec_td = trow.xpath('.//td[@data-stat="rec_td"]/text()').extract_first()
                rush_att = trow.xpath('.//td[@data-stat="rush_att"]/text()').extract_first()
                rush_yds = trow.xpath('.//td[@data-stat="rush_yds"]/text()').extract_first()
                rush_td = trow.xpath('.//td[@data-stat="rush_td"]/text()').extract_first()
                yield {player_url + " " + season + " rush": [season, player_name, recs, rec_yds, rec_td, rush_att, rush_yds, rush_td, attempts, completions, pass_ints, pass_tds, pass_yds,games, solo_tackles, ast_tackles, tackles, loss_tackles, sacks, ints, ints_tds, ints_yds, pds, fum_rec, fum_forced, fum_tds, fum_yds,player_url]}
            except:
                continue
            recs = 0
            rec_yds = 0
            rec_td = 0
            rush_att = 0
            rush_yds = 0
            rush_td = 0

        for trow in response.xpath('//div[@id="all_passing"]//tbody//tr'):
            try:
                season = trow.path('.//th[@data-stat="year_id"]/a/text()').extract_first()
                games_pass = trow.xpath('.//td[@data-stat="g"]/text()').extract_first()
                attempts=trow.xpath('.//td[@data-stat="pass_att"]/text()').extract_first()
                completions=trow.xpath('.//td[@data-stat="pass_cmp"]/text()').extract_first()
                pass_ints=trow.xpath('.//td[@data-stat="pass_int"]/text()').extract_first()
                pass_tds=trow.xpath('.//td[@data-stat="pass_td"]/text()').extract_first()
                pass_yds=trow.xpath('.//td[@data-stat="pass_yds"]/text()').extract_first()
                yield {player_url+ " " + season + " pass": [season, player_name, recs, rec_yds, rec_td, rush_att, rush_yds, rush_td, attempts, completions, pass_ints, pass_tds, pass_yds,games, solo_tackles, ast_tackles, tackles, loss_tackles, sacks, ints, ints_tds, ints_yds, pds, fum_rec, fum_forced, fum_tds, fum_yds,player_url]}

            except:
                continue
            attempts = 0
            completions=0
            pass_ints=0
            pass_tds=0
            pass_yds = 0

        for trow in response.xpath('//div[@id="all_receiving"]//tbody//tr'):
            try:
                season = trow.path('.//th[@data-stat="year_id"]/a/text()').extract_first()
                games_rec = trow.xpath('.//td[@data-stat="g"]/text()').extract_first()
                recs = trow.xpath('.//td[@data-stat="rec"]/text()').extract_first()
                rec_yds = trow.xpath('.//td[@data-stat="rec_yds"]/text()').extract_first()
                rec_td = trow.xpath('.//td[@data-stat="rec_td"]/text()').extract_first()
                rush_att = trow.xpath('.//td[@data-stat="rush_att"]/text()').extract_first()
                rush_yds = trow.xpath('.//td[@data-stat="rush_yds"]/text()').extract_first()
                rush_td = trow.xpath('.//td[@data-stat="rush_td"]/text()').extract_first()
                yield {player_url+ " " + season + " rec": [season, player_name, recs, rec_yds, rec_td, rush_att, rush_yds, rush_td, attempts, completions, pass_ints, pass_tds, pass_yds,games, solo_tackles, ast_tackles, tackles, loss_tackles, sacks, ints, ints_tds, ints_yds, pds, fum_rec, fum_forced, fum_tds, fum_yds,player_url]}

            except:
                continue
            recs = 0
            rec_yds = 0
            rec_td = 0
            rush_att = 0
            rush_yds = 0
            rush_td = 0
        for trow in response.xpath('//div[@id="all_defense"]//tbody//tr'):
            try:
                season = trow.path('.//th[@data-stat="year_id"]/a/text()').extract_first()
                games_d = trow.xpath('.//td[@data-stat="g"]/text()').extract_first()
                solo_tackles = trow.xpath('.//td[@data-stat="tackles_solo"]/text()').extract_first()
                ast_tackles = trow.xpath('.//td[@data-stat="tackles_assists"]/text()').extract_first()
                tackles = trow.xpath('.//td[@data-stat="tackles_total"]/text()').extract_first()
                loss_tackles = trow.xpath('.//td[@data-stat="tackles_loss"]/text()').extract_first()
                sacks = trow.xpath('.//td[@data-stat="sacks"]/text()').extract_first()
                ints = trow.xpath('.//td[@data-stat="def_int"]/text()').extract_first()
                ints_tds = trow.xpath('.//td[@data-stat="def_int_tds"]/text()').extract_first()
                ints_yds = trow.xpath('.//td[@data-stat="def_int_yds"]/text()').extract_first()
                pds = trow.xpath('.//td[@data-stat="pass_defended"]/text()').extract_first()
                fum_rec = trow.xpath('.//td[@data-stat="fumbles_rec"]/text()').extract_first()
                fum_forced = trow.xpath('.//td[@data-stat="fumbles_forced"]/text()').extract_first() 
                fum_tds = trow.xpath('.//td[@data-stat="fumbles_rec_td"]/text()').extract_first()
                fum_yds = trow.xpath('.//td[@data-stat="fumbles_rec_yds"]/text()').extract_first()
                yield {player_url+ " " + season + " def": [season, player_name, recs, rec_yds, rec_td, rush_att, rush_yds, rush_td, attempts, completions, pass_ints, pass_tds, pass_yds,games, solo_tackles, ast_tackles, tackles, loss_tackles, sacks, ints, ints_tds, ints_yds, pds, fum_rec, fum_forced, fum_tds, fum_yds,player_url]}

            except:
                continue
            solo_tackles=0
            ast_tackles=0
            tackles=0
            loss_tackles=0
            sacks=0
            ints=0
            ints_tds=0
            ints_yds=0
            pds=0
            fum_rec=0
            fum_forced=0
            fum_tds=0
            fum_yds=0
