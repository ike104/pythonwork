# -*- encoding: utf-8 -*-
import sys
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
                      u'スプレッド',#Spread
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
    #
    # Header の itemを返す
    #
    def getHeader(self,item,short=False):
        if item=='EAName':
            return self.contents[u'Strategy Tester Report']
        if item=='Symbol':
            if not short:#GBPJPY (Great Britain Pound vs Japanese Yen)          
                return self.contents[u'通貨ペア']
            else:# GBPJPY
                p = self.contents[u'通貨ペア']                
                return p[0:6]
        if item=='Period':
            if not short:#1\u6642\u9593\u8db3(H1)  2012.01.02 08:00 - 
                        #2014.12.26 16:00    (2012.01.02 - 2014.12.28)            
                return self.contents[u'期間']
            else:# 2012.01.02-2014.12.28
                p = self.contents[u'期間']                
                return p[len(p)-24:len(p)-14] + '-'+p[len(p)-11:len(p)-1]
        if item=='TestStart':
             p = self.contents[u'期間']                
             return p[len(p)-24:len(p)-14]
        if item=='TestEnd':
             p = self.contents[u'期間']                
             return p[len(p)-11:len(p)-1]
        if item=='TimeFrame':
                p = self.contents[u'期間']                  
                return p[p.find('(')+1:p.find(')')]
        if item=="Total trades":
            return self.contents[u'総取引数']
        if item=="Profit factor":
            return self.contents[u'プロフィットファクター']
        if item=="Maximal drawdown":
            if not short:# 58930.00 (4.94%)
                return self.contents[u'最大ドローダウン']
            else:# 4.94
                dd = self.contents[u'最大ドローダウン']
                return dd[dd.find('(')+1:dd.find(')')-1]                                 
        if item=="Parameters":
            return self.contents[u'パラメーター']
        if item=="Profit trades":
            if not short:
                return self.contents[u'勝率(%)']
            else:
                p = self.contents[u'勝率(%)']
                return p[p.find('(')+1:p.find(')')-1]                
        if item=="Short position won":
            if not short:
                return self.contents[u'ショートポジション(勝率%）']
            else:
                p = self.contents[u'ショートポジション(勝率%）']
                return p[p.find('(')+1:p.find(')')-1]                
        if item=="Long position won":
            if not short:# 77740.00 (6)
                return self.contents[u'ロングポジション(勝率%）']
            else: # 6
                p = self.contents[u'ロングポジション(勝率%）']
                return p[p.find('(')+1:p.find(')')-1]                
        if item=="Maximal consecutive count of wins":
            if not short:
                return self.contents[u'最大化'+u'連勝(トレード数)']
            else:
                p = self.contents[u'最大化'+u'連勝(トレード数)']
                return p[p.find('(')+1:p.find(')')]                
        if item=="Maximal consecutive count of losses":
            if not short:
                return self.contents[u'最大化'+u'連敗(トレード数)']
            else:
                p = self.contents[u'最大化'+u'連敗(トレード数)']
                return p[p.find('(')+1:p.find(')')]                
        if item=="Spread":
            return self.contents[u'スプレッド']
    
    # パラメータのdictを返す
    def geEAtParameters(self):
        para = self.contents[u'パラメーター']
        pl = {}
        for p in para.split(';'):
            pn = p.split('=')
            if len(pn)==2:
                pl.update({pn[0].lstrip():pn[1].lstrip()})
                #print pn[0] + ':' +pn[1]
        return pl
    # 新しいベースファイル名を作成する
    def getBaseOutputName(self):
        return  self.getHeader("EAName") + '-' \
                + self.getHeader("Symbol",True) \
                + self.getHeader("TimeFrame") + '-'\
                + self.getHeader("Period",True) \
                + 'x' + self.getHeader("Total trades")\
                + 'PF' + self.getHeader("Profit factor")\
                + 'DD' + self.getHeader("Maximal drawdown",True)   
"""
#----------------------------------------------------------------------------------- 
 MT4 TestReoprt.htmファイルを入力して、テスト結果を表す.htmファイルにコピーする。同時に
 テスト条件のパラメータファイル(.set)、結果を１行にまとめたサマリーファイル(.txt）を生成する。
 出力ディレクトリは指定可能で省略すると、"result"になる。
 出力ファイル名 例：
 result/ichimokuEA-GBPJPY-2012.01.02-2014.12.28x170PF1.71DD4.94.htm
 result/ichimokuEA-GBPJPY-2012.01.02-2014.12.28x170PF1.71DD4.94.set
 result/ichimokuEA-GBPJPY-2012.01.02-2014.12.28x170PF1.71DD4.94.txt
#----------------------------------------------------------------------------------- 
"""

def do_conv(infile,outputDir='result/'):
    
    if infile[0]=='"':
        infile = infile[1:]
    if infile[len(infile)-1]=='"':
        infile = infile[0:len(infile)-1]
        
    if outputDir[len(outputDir)-1] != '/':
        outputDir = outputDir + '/'
    print '\n'    
    print "Input file = ", infile
    print "Output dir = ", outputDir
    print '\n'    
    
    
    # 結果は　result/フォルダに入れる    
    import codecs as cdc
        
    try:
        f = cdc.open(infile,'rb','cp932')
    except IOError:
        sys.exit("\n Cannot open :"+infile)
    html = f.read()
    f.close()    
    
    rpt = MT4TestReport()
    rpt.feed(html)
    print "Data count = " + str(len(rpt.data_content))
    
    # 新しいファイル名を作成する
    fname    = rpt.getBaseOutputName()    
    giffile  = outputDir + fname+'.gif'
    giffname = fname+'.gif'
    htmfile  = outputDir + fname+'.htm'
    
    
    # パラメータをファイル名としたhtmファイルを作成
    import shutil
    # グラフのGIFを別名コピー
    shutil.copyfile(rpt.graph_file,giffile)
    # htmファイルのリンク先を書き換え
    print "replace = " + rpt.graph_file, giffname    
    html = html.replace(rpt.graph_file,giffname)
    # 新しいhtmファイルを書き出す
    fo = cdc.open(htmfile,'wb','cp932')
    fo.write(html)
    fo.close();
    
    print "\nCreated :"
    print " " + htmfile 
    print " " + giffile 
    print " "
    
    ##########  setファイルを作る
    setfile  = outputDir + fname+'.set'
    
    pl = rpt.geEAtParameters()
    
    sfile = open(setfile,'w')
    
    for p in pl.keys():
        sd = p + '=' + pl[p] + '\n' \
        + p + ',F=0' + '\n' \
        + p + ',1=' + pl[p] + '\n' \
        + p + ',2=0' + '\n' \
        + p + ',3=0' + '\n'
        #print sd
        sfile.write(sd)
    sfile.close()
    print "\nCreated :"
    print " " + setfile 


 ##########  summryファイルを作る
    sumfile  = outputDir + fname+'.txt'
    
    sumidx = ["Symbol","TimeFrame","Spread","EAName","TestStart", 
                "TestEnd","Total trades","Profit factor","Maximal drawdown",
                "Profit trades","Short position won","Long position won",
                "Maximal consecutive count of wins",
                "Maximal consecutive count of losses"]
    separator = '\t'
    
    idxdata=''    
    for i in sumidx:
        idxdata = idxdata + str(i) + separator
    
    idxdata = idxdata + 'ReportFile' + '\n'
    
    sumdata = ''    
    for i in sumidx:
        sumdata = sumdata + str(rpt.getHeader(i,True)) + separator
    sumdata = sumdata + str(rpt.getBaseOutputName()) + '.htm' + separator
    sumdata = sumdata + str(rpt.getHeader('Parameters',True))
    
    sfile = open(sumfile,'w')
    sfile.write(idxdata)
    sfile.write(sumdata)
    sfile.close()
    print "\nCreated :"
    print " " + sumfile 
    

def main(argv):
    
    
    if len(argv)<2:
        sys.exit("\nUsage: " + str(argv[0]) + " inputfile [outputdir=result]")
    
    infile = argv[1]
    outputDir = 'result/'
    if len(argv)>=3:
        outputDir = argv[2]
    if outputDir[len(outputDir)-1] != '/':
        outputDir = outputDir + '/'
    print '\n'    
    print "Input file = ", infile
    print "Output dir = ", outputDir
    print '\n'    
    #infile = 'IchimokuEA-GPBJPY1H 201202-201412 x170 PF1.71DD4.49.htm'
    do_conv(infile,outputDir)


if __name__ == '__main__':
    main(sys.argv)

    
