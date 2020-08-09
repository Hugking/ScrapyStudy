# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import copy

import scrapy


class BaseItem(scrapy.Item):
    """基本字段"""

    type = scrapy.Field()
    mysql_id = scrapy.Field()  # 用来存放存入mysql后的id
    url = scrapy.Field()  # 用来存放spider.url

    name = scrapy.Field()
    source = scrapy.Field()
    get_date = scrapy.Field()
    is_drop = scrapy.Field()  # 是否被逻辑删除的item，不能入库，但是入mongo，需要进入到lastpopeline
    is_err = scrapy.Field()  # 是否是管道里异常的item，不能入库，不入mongo，需要进入到lastpopeline计数

    status = scrapy.Field()  # 用来表示数据的状态 ， 在不同的表中的意义不尽相同。【通常】 0代表数据需要人工识别/补充 1表示数据已经入mysql库  -1表示数据错误/无效  等等
    is_effective = scrapy.Field()

    response_text = scrapy.Field()  # 此条数据的原始响应文本，通常会在中间件内进行赋值,也可自行赋值

    @property
    def title(self):
        """
        用于提取此条item中的标题字段，主要为了避免频繁硬编码，在不同数据中标题的字段名不同
        子类继承BaseItem后需要和以下类属方法搭配使用
        @property
        def __title__(cls):
            return 'management_info'

        """
        if self.__title__() in self.keys():
            return self[self.__title__()]

    def __repr__(self, must_be_print=[], could_be_print=[]):
        """在返回item时，这个方法会被自动调用，由于部分字段过长，这里进行了重写"""
        """在控制台上，不打印response_text(过长)，请务必确认此值拿到的正文文本是正确的"""
        """ 由于字段众多，只打印部分字段   """
        """打印的时候尽可能保持json/字典风格.
        ----->    为什么不直接以字典形式或json形式打印呢?答:首先字段会多出很多,而且很多可迭代对象的打印会出现原始编码而不是想要的字符形式
        """
        data = copy.deepcopy(dict(self))

        sentence = '{'
        if 'source_url' not in must_be_print:  # 原网页url必须打印
            must_be_print.append('source_url')

        for key in must_be_print:
            value = data.get(key, '')
            if isinstance(value, str):
                new_line = f'"{key}":"{value}",\n'  # 字符串就在外面多加了引号
            else:
                new_line = f'"{key}":"{str(value)}",\n'
            sentence += new_line

        for key in could_be_print:
            value = data.get(key, '')  # 只打印值不为空或0的数据
            if value:
                sentence += f'{key}:{value},\n'

        array = list(sentence)
        array[-1] = '}'
        array[-2] = ''  # 替换最后一个换行
        del data
        return ''.join(array)


class ProItem(BaseItem):

    @classmethod
    def __title__(cls):
        return 'project_name'

    project_date = scrapy.Field()  # 日期
    project_name = scrapy.Field()
    price = scrapy.Field()  # 如果是字符串，会在管道中进行处理，转成数字

    spider_id = scrapy.Field()

    def __repr__(self):
        could_be_print = [  # 一些可以为空的字段，将只打印有值且值不为0或空串的字段
        ]

        must_be_print = ['project_name', 'project_date', 'price']
        return super().__repr__(must_be_print, could_be_print)
