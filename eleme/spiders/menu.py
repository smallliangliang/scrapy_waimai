# -*- coding: utf-8 -*-
import json

import scrapy

from eleme import settings
from eleme.items import MenuItem
from eleme.mysqlhelper import *


class MenuSpider(scrapy.Spider):
    """获取商家菜单信息

    获取尚未获取menu的商家ID，拼接URL构建start_urls
    把结果交给pipeline
    """
    name = "menu"
    allowed_domains = ["ele.me"]
    base_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id="

    def start_requests(self):
        cur.execute("""
            SELECT restaurant_id FROM restaurant_info
            LEFT JOIN (SELECT restaurant_id AS id FROM menu_info) AS t
            ON restaurant_info.restaurant_id = t.id
            WHERE t.id IS NULL
        """)
        for restaurant_id in cur.fetchall():
            yield scrapy.Request(self.base_url + str(restaurant_id[0]))

    def parse(self, response):
        if 200 == response.status:
            item = MenuItem()
            item["menu"] = response.text
            item["restaurant_id"] = response.url.split("=")[-1]
            yield item
