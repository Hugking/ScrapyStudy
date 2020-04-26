import re
import scrapy
from bs4 import BeautifulSoup
from lxml import etree
from scrapy.http import Request
from ip.items import IpItem


class IpSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['proxy.mimvp.com']
    pages = 1
    base_url = 'https://proxy.mimvp.com/freeopen?proxy=in_hp&sort=&page='

    def start_requests(self):
        url = self.base_url + '1'
        yield Request(url, self.parse)

    def parse(self, response):
        max_num = response.xpath('//*[@id="listnav"]/ul/li[8]/a/text()').extract()[0]
        for num in range(1, int(max_num) + 1):
            url = self.base_url + str(num)
            yield Request(url, self.get_one_page)

    def get_one_page(self, response):
        item = IpItem()
        one_page_list = response.xpath('//*[@id="mimvp-body"]/div/table/tbody/tr').extract()  # 单个
        for i in range(len(one_page_list)):
            match_re = re.findall(r'<td.*?>(.*?)</td>', one_page_list[i])
            if len(match_re) != 0:
                item['ip'] = match_re[1]

                img_re = re.match(r'.*"(.*)">', match_re[2])
                if img_re:
                    item['port_img_urls'] = img_re.group(1)
                else:
                    item['port_img_urls'] = ''

                city_re = re.match(r'.*>(.*)<', match_re[5])
                if city_re:
                    item['city'] = city_re.group(1)
                else:
                    item['city'] = ''
            yield item
