# -*- encoding: utf-8 -*-
import csv
from HTMLParser import HTMLParser

class MT4TestReport(HTMLParser):
    """My HTMLParser for MT4 Test Report"""

    
    def __init__(self):
        HTMLParser.__init__(self)
        self.state = 0
        self.contents = {}
        self.cindex
        self.index = [u'通貨ペア',u'期間',u'モデル',u'パラメーター',u'テストバー数'
                      ,u'モデルティック数',u'モデリング品質',u'不整合チャートエラー',u'初期証拠金',
                      u'スプレッド',u'総損益',u'総利益',u'総損失',u'プロフィットファクター',u'期待利得',
                      u'絶対ドローダウン',u'最大ドローダウン',u'相対ドローダウン',u'総取引数',
                      u'ショートポジション(勝率%）',u'ロングポジション(勝率%）',u'勝率(%)',u'負率 (%)',
                      u'勝トレード',u'負トレード',u'連勝(金額)',u'連敗(金額)',u'連勝(トレード数)',u'連敗(トレード数)',
                      u'連勝',u'連敗']
        self.index_prefix = [u'最大',u'平均',u'最大化']
        self.header_prefix = u'Strategy Tester Report'
        self.ea_name = []
        self.server_name = ''
        self.graph_file_prefix = 'img src'
        self.graph_file = ''

    def handle_starttag(self, tag, attrs):
        if state == 0:
            pass
        elif state == 1:
            pass
        else:
            pass
            
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if state == 0:
            if data == self.header_prefix:
                self.ea_name = self.header_prefix
            else:
                if len(self.ea_name)>0:
                    self.ea_name = data
                    
                    
        elif state == 1:
            pass
        else:
            pass
            

#def main():
url = 'file:///F:/Users/ikechan/Documents/Pythonwork/IchimokuEA-GPBJPY1H%20201202-201412%20x170%20PF1.71DD4.49.htm'
import urllib2
response = urllib2.urlopen(url)
html = response.read()
response.close()

import lxml.html

#htm = html.decode('shift-JIS')
# Shift_JIS, cp932, EUC-JP, UTF-8
#dom = lxml.html.fromstring(html.decode('Shift_JIS'))
dom = lxml.html.fromstring(html)
title = dom.head.find('title').text_content()
EAName = title.split(':')[1].lstrip();
print "EA Name :"+EAName
body = dom.body
table1 = body.xpath('//table')[0]
a = table1.xpath('//tr')[0].text_content()

table2 = body.xpath('//table')[1]


   # parser = MT4TestReport()
   # parser.feed(html.decode('utf-8'))
   # parser.close()



#if __name__ == '__main__':
#  main()

    
