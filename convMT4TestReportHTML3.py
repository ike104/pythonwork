# -*- encoding: utf-8 -*-
import sys
import datetime 
from HTMLParser import HTMLParser

class MT4TestReport(HTMLParser):
    """Convert MT4 Test report .html """

    """
        MT4 report.htmファイルを読み込むクラス
         htmlファイルを読み込んで,feedするとデータが取り込まれる。
         　rpt = MT4TestReport()
         　rpt.feed(html)
    """
   
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
        #--------------------------------------------------------------
        # ｈｔｍｌが参照している.gifファイル名を返す        
        self.graph_file = '' # image file name
        self.data_start_index = u'残高'
        self.data_buf = [] # working buffer
        #--------------------------------------------------------------
        # トレードデータ(生）を返す        
        self.data_content = [] # Trade data
        #--------------------------------------------------------------
        # トレードデータ（modifyを含めた）を返す        
            #    
            # 0:index, 
            # 1:OpenTime,  2:Type,  3:Lots, 4:OpenPrice, 
            # 5:CloseTime, 6:Order, 7:Lots, 8:ClosePrice
            #　＊すべて文字列
        self.order = {}
        #--------------------------------------------------------------
        # トレードデータを返す（全トレード）        
        #  modify含めないデータ       
        self.totalorder = []
        #--------------------------------------------------------------
        # トレードデータを返す        
        #  modify含めないデータ       
        self.buyorder = []
        #--------------------------------------------------------------
        # トレードデータを返す        
        #  modify含めないデータ       
        self.sellorder = []
        #--------------------------------------------------------------
        # トレードプロフィット（通貨＊Lot）     
        #  各トレード毎の損益（float)
        self.totalprofit = []
        self.buyprofit = []
        self.sellprofit = []
        
    def handle_starttag(self, tag, attrs):
        if tag == self.graph_file_prefix:
            self.graph_file = attrs[0][1]
            #print 'Image file = ',self.graph_file
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
                    #print self.ind_pre,self.ind,data
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
    def doConv(self):
        tmpd = {}
        for ord in self.data_content:
            if ord[2] != 'modify':
                idx = int(ord[3])
                if tmpd.has_key(idx):
                    no = [tmpd.get(idx),
                    [int(ord[0]),
                    datetime.datetime.strptime(ord[1],'%Y.%m.%d %H:%M'),
                    str(ord[2]),int(ord[3]),float(ord[4]),
                    float(ord[5]),float(ord[6]),float(ord[7])]
                    ]            
                else:
                    no = [int(ord[0]),
                    datetime.datetime.strptime(ord[1],'%Y.%m.%d %H:%M'),
                    str(ord[2]),int(ord[3]),
                    float(ord[4]),float(ord[5]),float(ord[6]),float(ord[7])]
                tmpd.update({idx:no})        

        okey = {'sell','buy'}
        ckey = {'close','t/p','s/l'}
        for i in tmpd.keys():
            d = tmpd.get(i)
            if okey.issuperset({d[0][2]}) and ckey.issuperset({d[1][2]}):
                opnord = d[0]
                clsord = d[1]
            elif okey.issuperset({d[1][2]}) and ckey.issuperset({d[0][2]}):
                opnord = d[1]
                clsord = d[0]
            else:
                continue
            #    
            # 0:index, 
            # 1:OpenTime,  2:Type,  3:Lots, 4:OpenPrice, 
            # 5:CloseTime, 6:Order, 7:Lots, 8:ClosePrice
            #
            o = [i,opnord[1],opnord[2],opnord[4],opnord[5],
                 clsord[1],clsord[2],clsord[4],clsord[5]]
            self.order.update({i:o})  
        
             
        for i in self.order.keys():
            o = self.order.get(i)
            if o[2]=='buy':
                self.buyorder.append(o)
            if o[2]=='sell':
                self.sellorder.append(o)
            self.totalorder.append(o)
        
        for i in self.totalorder:
            if i[2]=='buy':    
                self.totalprofit.append(i[7]*i[8]-i[3]*i[4])
            if i[2]=='sell':    
                self.totalprofit.append(-i[7]*i[8]+i[3]*i[4])
        
        for i in self.buyorder:
            self.buyprofit.append(i[7]*i[8]-i[3]*i[4])
        
        for i in self.sellorder:
            self.sellprofit.append(-i[7]*i[8]+i[3]*i[4])
        
    def feed(self,data):
        """
        override -- 
        """
        HTMLParser.feed(self,data)
        self.doConv()
        
    def getHeader(self,item,short=False):
        """ -------------------------------------
        Header の itemを返す
        """        
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
        if item=="Initial deposit":
            return self.contents[u'初期証拠金']
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
    def geEAtParameters(self):
        """ 
        パラメータのdictを返す
        """        
        para = self.contents[u'パラメーター']
        pl = {}
        for p in para.split(';'):
            pn = p.split('=')
            if len(pn)==2:
                pl.update({pn[0].lstrip():pn[1].lstrip()})
                #print pn[0] + ':' +pn[1]
        return pl
    def getBaseOutputName(self):
        """
        新しいベースファイル名を作成する
        """        
        return  self.getHeader("EAName") + '-' \
                + self.getHeader("Symbol",True) \
                + self.getHeader("TimeFrame") + '-'\
                + self.getHeader("Period",True) \
                + 'x' + self.getHeader("Total trades")\
                + 'PF' + self.getHeader("Profit factor")\
                + 'DD' + self.getHeader("Maximal drawdown",True)   
    def isTradeTypeBuy(self,orderNum):
        return self.order[orderNum][2] == 'buy'
    def isTradeTypeSell(self,orderNum):
        return self.order[orderNum][2] == 'sell'
    def tradeProfit(self,orderNum):
        i = self.order[orderNum]
        if self.isTradeTypeBuy(orderNum):
           return i[7]*i[8]-i[3]*i[4]
        if self.isTradeTypeSell(orderNum):
           return -i[7]*i[8]+i[3]*i[4]
    def tradePeriod(self,orderNum):
        i = self.order[orderNum]
        return i[5] - i[1]
           
"""
#----------------------------------------------------------------------------------- 
 MT4 TestReoprt.htmファイルを入力して、テスト結果を表す.htmファイルにコピーする。同時に
 
#----------------------------------------------------------------------------------- 
"""
import matplotlib.pylab as plt
import numpy as np
import codecs as cdc

def tradeanalyze(rpt):
    #print "Data count = " + str(len(rpt.data_content))
    
    print "\n--------------------------------------------" 
    print "- Trades count \n"
    
    lotvol = 1
    
    tpro = np.array(rpt.totalprofit)*lotvol
    bpro = np.array(rpt.buyprofit)*lotvol
    spro = np.array(rpt.sellprofit)*lotvol
    
    #fig, axes = plt.subplots(nrows=2, ncols=3)
    #fig.tight_layout() # Or equivalently,  "plt.tight_layout()"
    print " "    
    wc = len(rpt.buyprofit)
    lc = len(rpt.sellprofit)
    print "Total trades = %5d" % (wc+lc)
    print "Long  trades = %5d (%6.2f %%)" %  (wc,100*float(wc)/float(wc+lc))
    print "Short trades = %5d (%6.2f %%)" %  (lc,100*float(lc)/float(wc+lc))
    
    print "\n--------------------------------------------" 
    print "- Profit \n"
    plt.figure(figsize=(10,3))
    plt.subplot(121)
    plt.title("total profit")
    plt.plot(np.cumsum(tpro))
    plt.subplot(122)
    plt.hist(tpro,bins=30)
    plt.savefig("test11.png")
    plt.show()
    
    plt.figure(figsize=(10,3))
    plt.subplot(121)
    plt.title("buy profit")
    plt.plot(np.cumsum(bpro))
    plt.subplot(122)
    plt.hist(bpro,bins=30)
    plt.savefig("test12.png")
    plt.show()
    
    plt.figure(figsize=(10,3))
    plt.subplot(121)
    plt.title("sell profit")
    plt.plot(np.cumsum(spro))
    plt.subplot(122)
    plt.hist(spro,bins=30)
    plt.savefig("test13.png")
    plt.show()
    
    bw = []
    bl = []
    sw = []
    sl = []
    for o in rpt.order.keys():
        if rpt.isTradeTypeBuy(o):
            if rpt.tradeProfit(o) > 0:
                bw.append(o)
            else:
                bl.append(o)
        if rpt.isTradeTypeSell(o):
            if rpt.tradeProfit(o) > 0:  
                sw.append(o)
            else:
                sl.append(o)
    
    wc = len(bw)
    lc = len(bl)
    print "Long  profit rate = %6.2f %% [ %3d / %3d ]" % \
                 (100*float(wc)/float(wc+lc),wc,lc+wc )                   
    wc = len(sw)
    lc = len(sl)
    print "Short profit rate = %6.2f %% [ %3d / %3d ]" % \
                 (100*float(wc)/float(wc+lc),wc,lc+wc )                   
    

def tradeanalyze2(rpt):
    #print "Data count = " + str(len(rpt.data_content))
    #
    # トレード期間のヒストグラムを描画する
    #
    print "\n--------------------------------------------" 
    print "- Holding period \n"
    f = filter(lambda n:n[8]-n[4]>0 ,rpt.buyorder)
    tw = []    
    for n in f:
        d = n[5]-n[1]
        tw.append(float((d.total_seconds()/60./60.)))
    f = filter(lambda n:n[8]-n[4]<=0 ,rpt.buyorder)
    tl = []    
    for n in f:
        d = n[5]-n[1]
        tl.append(float((d.total_seconds()/60./60.)))
    plt.figure(figsize=(10,3))    
    plt.subplot(121)        
    plt.hist(tw,bins=30,color='b',alpha = 0.5,label='win')
    plt.hist(tl,bins=30,color='r',alpha = 0.5,label='loss')
    plt.title('Trading period(Hour),Long')
    plt.legend()
    plt.xlabel('Hour(s)')
    plt.ylabel('Times')    
    # plt.show()
    #-----------------------------------------------
    f = filter(lambda n:n[8]-n[4]>0 ,rpt.sellorder)
    tw = []    
    for n in f:
        d = n[5]-n[1]
        tw.append(float((d.total_seconds()/60./60.)))
    f = filter(lambda n:n[8]-n[4]<=0 ,rpt.sellorder)
    tl = []    
    for n in f:
        d = n[5]-n[1]
        tl.append(float((d.total_seconds()/60./60.)))
            
    plt.subplot(122) 
    plt.hist(tw,bins=30,color='b',alpha = 0.5,label='win')
    plt.hist(tl,bins=30,color='r',alpha = 0.5,label='loss')
    plt.title('Trading period(Hour),Short')
    plt.legend()
    plt.xlabel('Hour(s)')
    plt.ylabel('Times')    
    plt.savefig("test2.png")
    plt.show()

#-----------------------------------------------------
def winlossCount(ord):
    pc,nc=0,0
    for i in ord:    
        if i[2] == 'buy':
            f = 1
        else:
            f = -1
        if f*(i[8]-i[4])>0:
            pc = pc+1
        else:
            nc = nc+1
    return (pc,nc)
    
    
def tradeanalyze3(rpt):
   # print "Data count = " + str(len(rpt.data_content))
    print "\n--------------------------------------------" 
    print "- Entry \n "
     #
    # エントリー時刻毎の勝率
    #
    
    print "Hour  : profit rate[win/total]"    
    dat = []    
    for t in range(0,24):
        f = filter(lambda n:n[1].hour==t ,rpt.totalorder)
        pc,nc = winlossCount(f)
        if pc+nc>0:
            dat.append(100*float(pc)/float(pc+nc))            
            print " %2d H : %6.2f %% [ %3d / %3d ]" % \
                (t,100*float(pc)/float(pc+nc),pc,(pc+nc))
    
    plt.figure(figsize=(5,2))    
    x   = range(len(dat))
    xt  = [ str(s) + 'H' for s in x]
    plt.title("$Profit rate by Entry hour$")    
    plt.ylim(0,100)
    plt.xlim(-1,len(dat)+1)
    plt.xticks(x,xt,rotation=90)
    plt.axhline(50,color='r')
    plt.bar(x,dat,align='center',alpha=0.7) 
    plt.savefig("test31.png")
    plt.show()
    
    #
    # エントリー曜日毎の勝率
    #
    print ""
    print "Weekday  : profit rate[win/total]"
    week = ['mon','tue','wed','thu','fri','sat','sun']    
    dat = []    
    for t in range(0,7):
        f = filter(lambda n:n[1].weekday()==t ,rpt.totalorder)
        pc,nc = winlossCount(f)
        if pc+nc>0:
            dat.append(100*float(pc)/float(pc+nc))            
            print "%s      : %6.2f %% [ %3d / %3d ]" % \
                (week[t],100*float(pc)/float(pc+nc),pc,(pc+nc))
    
    plt.figure(figsize=(5,2))    
    x   = range(len(dat))
    plt.title("$Profit rate by Entry weekday$")    
    plt.ylim(0,100)
    plt.xlim(-1,len(dat)+1)
    plt.xticks(x,week,rotation=90)
    plt.axhline(50,color='r')
    plt.bar(x,dat,align='center',alpha=0.7) 
    plt.savefig("test32.png")
    plt.show()

def tradeanalyze4(rpt):
    #print "Data count = " + str(len(rpt.data_content))
    #
    # エントリー時刻毎の勝率
    #
    print "\n--------------------------------------------" 
    print "- Exit  \n"
    print 'Entry -> Exit : profit rate [win/total]'    
    cc = []
    cd = []
    for t in ['close','t/p','s/l']:
        f = filter(lambda n:n[6]==t ,rpt.buyorder)
        cc.append(len(f))        
        pc,nc = winlossCount(f)
        if pc+nc>0:
            cd.append(100*float(pc)/float(pc+nc))
            print "Long ->%6s : %6.2f %% [ %3d / %3d ]" % \
                (t,100*float(pc)/float(pc+nc),pc,(pc+nc))
        else:
            cd.append(0.)
    for t in ['close','t/p','s/l']:
        f = filter(lambda n:n[6]==t ,rpt.sellorder)
        cc.append(len(f))        
        pc,nc = winlossCount(f)
        if pc+nc>0:
            cd.append(100*float(pc)/float(pc+nc))
            print "Short->%6s : %6.2f %% [ %3d / %3d ]" % \
                (t,100*float(pc)/float(pc+nc),pc,(pc+nc))
        else:
            cd.append(0.)

    s = np.array([cd[0],cd[1],cd[2]])
    b = np.array([cd[3],cd[4],cd[5]])
    
    x = np.array(range(len(s)))
    xt = ['close','t/p','s/l']
    gw = 0.4
    plt.figure(figsize=(5,2))
    plt.title('$Profit rate by exit $')
    plt.xlabel("Profit rate")
    plt.xlim(0,100)
    #plt.ylim(0+0.5,5-0.5)    
    plt.yticks(x,xt)
    plt.grid(True)
    plt.barh(x -gw/2, s, height = gw, align='center',color='b',alpha=0.5,\
            label='Short')
    plt.barh(x +gw/2, b, height = gw, align='center',color='g',alpha=0.5,\
            label='Long'    )
    plt.legend()
    plt.axvline(50,color='r')
    plt.savefig("test41.png")
    plt.show()
    

    ac = cc[0]+cc[3]
    tc = cc[1]+cc[4]
    sc = cc[2]+cc[5]
    tc = ac+tc+sc    

    
    print " "
    print "Exit  : count (rate)" 
    print "Close : %4d (%6.2f %%)" % (ac, float(ac)/float(tc))
    print "t/p   : %4d (%6.2f %%)" % (tc, float(tc)/float(tc))
    print "s/l   : %4d (%6.2f %%)" % (sc, float(sc)/float(tc))

    from matplotlib import cm
    names =[ 'close','t/p', 's/l']
    # それぞれの割合を用意
    ratios = [ac, tc,sc]
    # どれだけ飛び出すか指定
    moves=(0, 0, 0)
    # 適当なカラーをマッピング
    col = cm.Set2(np.arange(3)/3.,0.7)
    # 円グラフを描画（影付き）
    plt.pie(ratios, explode=moves, labels=names, autopct='%1d%%',\
    shadow=True,colors=col)
    # 円グラフ他ので縦横比は等しく
    plt.gca().set_aspect('equal')
    plt.title('$Exit count$')
    plt.savefig("test42.png")
    plt.show()

#infile = 'EnvelopeEA009-USDJPY15M x677 PF1.93 DD5.12.htm'
#tradeanalyze(infile)

import os
inputDir = 'convMT2TestReport/result'
for fn in os.listdir(inputDir):
    if fn.endswith(".htm") and fn[0] != '_':
        infile = str(inputDir + '/'+ fn )
        print "\n\n=================================================="
        print " Inputfile =", infile
        try:
            f = cdc.open(infile,'rb','cp932')
        except IOError:
            sys.exit("\n Cannot open :"+infile)
        html = f.read()
        f.close()    
    
        rpt = MT4TestReport()
        rpt.feed(html)
        tradeanalyze(rpt)
        tradeanalyze2(rpt)
        tradeanalyze3(rpt)
        tradeanalyze4(rpt)
        
        

#def main(argv):
    
    

#if __name__ == '__main__':
#    main(sys.argv)

    
