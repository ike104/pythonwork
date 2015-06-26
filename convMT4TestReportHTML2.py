# -*- encoding: utf-8 -*-
import csv
from HTMLParser import HTMLParser

class MT4TestReport(HTMLParser):
    """Convert MT4 Test report .html """

    
    def __init__(self):
        HTMLParser.__init__(self)
        self.state = 0 # working 
        self.contents = {} # Header data
        self.index = [
                      u'Strategy Tester Report',
                      u'通貨ペア',#Symbol
                      u'期間',#Period
                      u'モデル',#Model
                      u'パラメーター',#Parameters
                      u'テストバー数',#Bars in test
                      u'モデルティック数',#Tick modelled
                      u'モデリング品質',#Modelling quality
                      u'不整合チャートエラー',#Mismatched charts errors
                      u'初期証拠金',#Initial deposit
                      u'スプレッド',#spread
                      u'総損益',#Total net profit
                      u'総利益',#Gross profit
                      u'総損失',#gross loss
                      u'プロフィットファクター',#Profit factor
                      u'期待利得',#Expected payoff
                      u'絶対ドローダウン',#Absolute drawdown
                      u'最大ドローダウン',#Maximal drawdown
                      u'相対ドローダウン',#Relative drawdown
                      u'総取引数',#Total trades
                      u'ショートポジション(勝率%）',#Short position(won %)
                      u'ロングポジション(勝率%）',#Long position(won %)
                      u'勝率(%)',#Profit trades(% of total)
                      u'負率 (%)',#Loss trades(% of total)
                      u'勝トレード',#Largest/Average profit trade
                      u'負トレード',#Largest/Average loss trade
                      u'連勝(金額)',#Maximum consecutive wins(profit in money)
                      u'連敗(金額)',#Maximum consecutive losses(profit in money)
                      u'連勝(トレード数)',#Maximal consecutive profit(count of wins)
                      u'連敗(トレード数)',#Maximal consecutive loss(count of losses)
                      u'連勝',#Average consecutive wins
                      u'連敗',#Average consecutive losses
                      ]
        self.index_prefix = [
                      u'最大',#Maximum
                      u'平均',#Average
                      u'最大化'#Maximal
                      ]
        self.ind = '' # working buffer
        self.ind_pre = '' # working buffer
        self.graph_file_prefix = 'img'
        self.graph_file = '' # image file name
        self.data_start_index = u'残高'
        self.data_buf = [] # working buffer
        self.data_content = [] # Trade data
        
    def handle_starttag(self, tag, attrs):
        if tag == self.graph_file_prefix:
            self.graph_file = attrs[0][1]
            print 'Image file = ',self.graph_file
    def handle_endtag(self, tag):
        if self.state == 1:# Data mode
            if tag == 'tr': # end of table row
               if len(self.data_buf) > 0: 
                   self.data_content.append(self.data_buf)
                   self.data_buf = []

    def handle_data(self, data):
        data = data.lstrip().rstrip()
        if len(data)>0:
            #print data
            if self.state == 0:# Header mode
                if len(self.ind)>0:
                    print self.ind_pre,self.ind,data
                    self.contents.update({self.ind_pre + self.ind:data})
                    self.ind = ''
                if data in self.index:
                    self.ind = data
                if data in self.index_prefix:
                    self.ind_pre = data
                if data ==  self.data_start_index:
                    self.state = 1# Data mode
            elif self.state == 1:
                self.data_buf.append(data)
            else:
                pass
    def getHeader(self,item):
        if item=='EAName':
            return self.contents[u'Strategy Tester Report']
        if item=='Symbol':
            return self.contents[u'通貨ペア']
        if item=='Period':
            return self.contents[u'期間']
        if item=="Total trades":
            return self.contents[u'総取引数']
        if item=="Profit factor":
            return self.contents[u'プロフィットファクター']
        if item=="Maximal drawdown":
            return self.contents[u'最大ドローダウン']
        if item=="Parameters":
            return self.contents[u'パラメーター']
 
#def main():

import codecs as cdc
infile = 'IchimokuEA-GPBJPY1H 201202-201412 x170 PF1.71DD4.49.htm'

f = cdc.open(infile,'rb','cp932')
html = f.read()

rpt = MT4TestReport()
rpt.feed(html)
print "Data count = " + str(len(rpt.data_content))

# 新しいファイル名を作成する
fname = rpt.getHeader("EAName") + '-'+ rpt.getHeader("Symbol")[0:6]
p = rpt.getHeader("Period")
timeframe =  p[p.find('(')+1:p.find(')')]
period    = p[len(p)-24:len(p)-14] + '-'+p[len(p)-11:len(p)-1]
fname = fname + '-' + period
fname = fname + 'x' + rpt.getHeader("Total trades")
fname = fname + 'PF' + rpt.getHeader("Profit factor")
dd = rpt.getHeader("Maximal drawdown")
fname = fname +'DD' + dd[dd.find('(')+1:dd.find(')')-1]                                 
giffname = fname+'.gif'
htmfile  = fname+'.htm'

# パラメータをファイル名としたhtmファイルを作成
import shutil
# グラフのGIFを別名コピー
shutil.copyfile(rpt.graph_file,giffname)
# htmファイルのリンク先を書き換え
html.replace(rpt.graph_file,giffname)
# 新しいhtmファイルを書き出す
fo = cdc.open(htmfile,'wb','cp932')
fo.write(html)
fo.close();

print "\nCreated :"
print " " + htmfile 
print " " + giffname 
print " "

##########  setファイルを作る
setfile  = fname+'.set'
para = rpt.getHeader("Parameters")
pl = {}
for p in para.split(';'):
    pn = p.split('=')
    if len(pn)==2:
        pl.update({pn[0].lstrip():pn[1].lstrip()})
        #print pn[0] + ':' +pn[1]

sfile = open(setfile,'w')

for p in pl.keys():
    sd = p + '=' + pl[p] + '\n'  + p + ',F=0'  + '\n' + p + ',F=1'  + '\n' +p + ',F=2' + '\n' 
    print sd
    sfile.write(sd)
sfile.close()
print "\nCreated :"
print " " + setfile 

#if __name__ == '__main__':
#  main()

    
