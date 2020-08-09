# -* coding:utf-8 -*-
"""
@author: wkaanig
@file: run_by_one_finger.py
@desc: 一根手指运行spider文件？
步骤：
1.在运行run_by_one_finger时添加参数：  $FileNameWithoutAllExtensions$
2.更改run的快捷键为 双击鼠标中键
3.选中你的文件 双击滚轮吧
"""

import sys

from scrapy import cmdline

file_name = sys.argv[1]
cmdline.execute(f"scrapy crawl {file_name}".split())

# from scrapy.cmdline import execute
#
# execute(['scrapy', 'crawl', 'ip'])
