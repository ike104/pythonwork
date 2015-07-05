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
#---------------------------------------------------------------------------- 
 MT4 TestReoprt.htmファイルを入力して、内容を分析する
 　・ *Analize.htm ファイルに出力
  ・ Long,Short毎の勝率、プロフィットカーブ
  ・ プロフィット・ロスの価格帯のヒストグラム  
  ・ エントリ時間、曜日ごとの勝率
  ・ エグジット毎の勝率
#----------------------------------------------------------------------------- 
"""
import matplotlib.pylab as plt
import numpy as np
import codecs as cdc

def tradeanalyze(rpt,fname,outputDir,data):
    """ 解析
    
    """    
    print "\n--------------------------------------------" 
    print "- Trades count \n"
    
        
    tpro = np.array(rpt.totalprofit)
    bpro = np.array(rpt.buyprofit)
    spro = np.array(rpt.sellprofit)
    
    #fig, axes = plt.subplots(nrows=2, ncols=3)
    #fig.tight_layout() # Or equivalently,  "plt.tight_layout()"
    print " "    
    wc = len(rpt.buyprofit)
    lc = len(rpt.sellprofit)
    t0= "%5d" % (wc+lc)
    t1 = "%5d (%6.2f %%)" %  (wc,100*float(wc)/float(wc+lc))
    t2 = "%5d (%6.2f %%)" %  (lc,100*float(lc)/float(wc+lc))
    print "Total trades = " + t0
    print "Long  trades = " + t1
    print "Short trades = " + t2 
    data.update({'$$T001001$$':t0})    
    data.update({'$$T001002$$':t1})    
    data.update({'$$T001003$$':t2})    
    
    print "\n--------------------------------------------" 
    print "- Profit \n"
    plt.figure(figsize=(8,2))
    plt.subplot(121)
    plt.title("total profit")
    plt.xlabel("time")    
    plt.ylabel("profit/loss")    
    plt.plot(np.cumsum(tpro))
    plt.subplot(122)
    plt.hist(tpro,bins=30)
    plt.title("total profit histgram")
    plt.xlabel("profit/loss")    
    plt.savefig(outputDir+fname+"test11.png",dpi=72)
    data.update({'$$I001001$$':fname+"test11.png"})    
    #plt.show()
    plt.draw()
    
    plt.figure(figsize=(8,2))
    plt.subplot(121)
    plt.title("long profit")
    plt.xlabel("time")    
    plt.ylabel("profit/loss")    
    plt.plot(np.cumsum(bpro))
    plt.subplot(122)
    plt.hist(bpro,bins=30)
    plt.title("long profit histgram")
    plt.xlabel("profit/loss")    
    plt.savefig(outputDir+fname+"test12.png",dpi=72)
    data.update({'$$I001002$$':fname+"test12.png"})    
    #plt.show()
    plt.draw()
    
    plt.figure(figsize=(8,2))
    plt.subplot(121)
    plt.title("short profit")
    plt.xlabel("time")    
    plt.ylabel("profit/loss")    
    plt.plot(np.cumsum(spro))
    plt.subplot(122)
    plt.hist(spro,bins=30)
    plt.title("short profit histgram")
    plt.xlabel("profit/loss")    
    plt.savefig(outputDir+fname+"test13.png",dpi=72)
    data.update({'$$I001003$$':fname+"test13.png"})    
    #plt.show()
    plt.draw()
    
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
    t0 = "%6.2f %% [ %3d / %3d ]" % (100*float(wc)/float(wc+lc),wc,lc+wc )
    print "Long  profit rate = " + t0                   
    wc = len(sw)
    lc = len(sl)
    t1 = "%6.2f %% [ %3d / %3d ]" % (100*float(wc)/float(wc+lc),wc,lc+wc )                   
    print "Short profit rate = "+ t1
    data.update({'$$T001004$$':t0})    
    data.update({'$$T001005$$':t1})    
    plt.close('all')    
 
    

def tradeanalyze2(rpt,fname,outputDir,data):
    """ トレード期間のヒストグラムを描画する
    
    """
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
    plt.figure(figsize=(8,2))    
    plt.subplot(121)        
    plt.hist(tw,bins=30,color='b',alpha = 0.5,label='win')
    plt.hist(tl,bins=30,color='r',alpha = 0.5,label='loss')
    plt.title('Trading period(Hour),Long')
    plt.legend()
    plt.xlabel('Hour(s)')
    plt.ylabel('Times')    
    # plt.show()
    plt.draw()
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
    plt.savefig(outputDir+fname+"test2.png",dpi=72)
    data.update({"$$I002001$$":fname+"test2.png"})    
    #plt.show()
    plt.draw()
    plt.close('all')    

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
    
    
def tradeanalyze3(rpt,fname,outputDir,data):
    """ エントリー時刻毎の勝率
    
    """
    print "\n--------------------------------------------" 
    print "- Entry \n "
    
    print "Hour  : profit rate[win/total]"    
    dat = []    
    for t in range(0,24):
        f = filter(lambda n:n[1].hour==t ,rpt.totalorder)
        pc,nc = winlossCount(f)
        if pc+nc>0:
            dat.append(100*float(pc)/float(pc+nc))            
            t0 = " %2d H : " % (t)             
            t1 = "%6.2f %% [ %3d / %3d ]" % (100*float(pc)/float(pc+nc),pc,\
                (pc+nc))          
            print t0 + t1
            t3 = "$$T0020%02d$$" % (t+1)            
            data.update({t3:t1})
    
    plt.figure(figsize=(5,3))    
    x   = range(len(dat))
    xt  = [ str(s) + 'H' for s in x]
    plt.title("Profit rate by Entry hour")    
    plt.ylim(0,100)
    plt.xlim(-1,len(dat)+1)
    plt.xticks(x,xt,rotation=90)
    plt.axhline(50,color='r')
    plt.bar(x,dat,align='center',alpha=0.7) 
    plt.savefig(outputDir+fname+"test31.png",dpi=72)
    data.update({'$$I003001$$':fname+"test31.png"})    
    #plt.show()
    plt.draw()
    
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
            t0 = "%6.2f %% [ %3d / %3d ]" % (100*float(pc)/float(pc+nc),pc,\
                (pc+nc))           
            dat.append(100*float(pc)/float(pc+nc))            
            t1 = "%s      : " % (week[t])            
            print t1 + t0
            t3 = "$$T0030%02d$$" % (t+1)
            data.update({t3:t0})
    plt.figure(figsize=(5,3))    
    x   = range(len(dat))
    plt.title("Profit rate by Entry weekday")    
    plt.ylim(0,100)
    plt.xlim(-1,len(dat)+1)
    plt.xticks(x,week,rotation=90)
    plt.axhline(50,color='r')
    plt.bar(x,dat,align='center',alpha=0.7) 
    plt.savefig(outputDir+fname+"test32.png",dpi=72)
    data.update({'$$I003002$$':fname+"test32.png"})    
    #plt.show()
    plt.draw()
    plt.close('all')    

def tradeanalyze4(rpt,fname,outputDir,data):
    
    """ エグジット要因ごとの勝率
    
    """
    print "\n--------------------------------------------" 
    print "- Exit  \n"
    print 'Entry -> Exit : profit rate [win/total]'    
    cc = []
    cd = []
    count = 1
    for t in ['close','t/p','s/l']:
        f = filter(lambda n:n[6]==t ,rpt.buyorder)
        cc.append(len(f))        
        pc,nc = winlossCount(f)
        if pc+nc>0:
            t0 = "%6.2f %% [ %3d / %3d ]" % (100*float(pc)/float(pc+nc),pc,\
            (pc+nc))            
            cd.append(100*float(pc)/float(pc+nc))
            t1 = "Long - %6s : " % (t)            
            print t1 + t0
            t3 = "$$T0040%02d$$" % (count)  
            count = count+1
            data.update({t3:t0})
        else:
            t3 = "$$T0040%02d$$" % (count)
            count = count+1
            data.update({t3:'NA'})
            cd.append(0.)
    for t in ['close','t/p','s/l']:
        f = filter(lambda n:n[6]==t ,rpt.sellorder)
        cc.append(len(f))        
        pc,nc = winlossCount(f)
        if pc+nc>0:
            t0 = "%6.2f %% [ %3d / %3d ]" % (100*float(pc)/float(pc+nc),pc,\
                (pc+nc))           
            cd.append(100*float(pc)/float(pc+nc))
            t1 = "Short- %6s : " % (t)            
            print t1 + t0
            t3 = "$$T0040%02d$$" % (count)  
            count = count+1
            data.update({t3:t0})
        else:
            t3 = "$$T0040%02d$$" % (count)
            count = count+1
            data.update({t3:'NA'})
            cd.append(0.)

    s = np.array([cd[0],cd[1],cd[2]])
    b = np.array([cd[3],cd[4],cd[5]])
    
    x = np.array(range(len(s)))
    xt = ['close','t/p','s/l']
    gw = 0.4
    plt.figure(figsize=(5,2))
    plt.title('Profit rate by exit ')
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
    plt.savefig(outputDir+fname+"test41.png",dpi=72)
    data.update({'$$I004001$$':fname+"test41.png"})       
    #plt.show()
    plt.draw()
    

    ac = cc[0]+cc[3]
    tc = cc[1]+cc[4]
    sc = cc[2]+cc[5]
    tt = ac+tc+sc    

    
    print " "
    t0 = "%6.2f %% [ %4d / %4d ]" % (100*float(ac)/float(tt),ac,tt)
    t1 = "%6.2f %% [ %4d / %4d ]" % (100*float(tc)/float(tt),tc,tt)   
    t2 = "%6.2f %% [ %4d / %4d ]" % (100*float(sc)/float(tt),sc,tt)
    print "Exit  : rate [count/total]" 
    print "Close : " + t0
    print "t/p   : " + t1
    print "s/l   : " + t2
    data.update({'$$T005001$$':t0})    
    data.update({'$$T005002$$':t1})    
    data.update({'$$T005003$$':t2})    
    
    from matplotlib import cm
    plt.figure(figsize=(2,2))
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
    plt.title('Exit count')
    plt.savefig(outputDir+fname+"test42.png",dpi=72)
    data.update({'$$I004002$$':fname+"test42.png"})       
    #plt.show()
    plt.draw()
    plt.close('all')    


def headeranalyze(rpt,fname,outputDir,data):
    """    # ヘッダーの解析
    
    
    """
    data.update({'$$TITLE$$': str(rpt.getHeader('EAName',True))})
    data.update({'$$EANAME$$': str(rpt.getHeader('EAName',True))})
    data.update({'$$TIMEFRAME$$': str(rpt.getHeader('TimeFrame',True)) })
    data.update({'$$SIMPERIOD$$': str(rpt.getHeader('Period',True))})
    data.update({'$$HTMLFILE$$': fname+'.htm'})
    data.update({'$$EAPARAM$$': str(rpt.getHeader('Parameters',True))})
    
    data.update({'$$SYMBOL$$': str(rpt.getHeader('Symbol',True))})
    data.update({'$$PERIOD$$': str(rpt.getHeader('TimeFrame',True))})
    data.update({'$$TOTALTRADE$$': str(rpt.getHeader('Total trades',True))})
    data.update({'$$PF$$': str(rpt.getHeader('Profit factor',True))})
    data.update({'$$DD$$': str(rpt.getHeader('Maximal drawdown',True))})
    data.update({'$$WINRATE$$': str(rpt.getHeader('Profit trades',True))})
    data.update({'$$LONGWINRATE$$':
     str(rpt.getHeader('Long position won',True))})
    data.update({'$$SHORTWINRATE$$':
     str(rpt.getHeader('Short position won',True)) })
    data.update({'$$CONSECTIVEWINS$$':
     str(rpt.getHeader('Maximal consecutive count of wins',True)) })
    data.update({'$$CONSECTIVELOSSES$$':
     str(rpt.getHeader('Maximal consecutive count of losses',True))})
    data.update({'$$000001$$':fname+'.gif'})
      
#infile = 'EnvelopeEA009-USDJPY15M x677 PF1.93 DD5.12.htm'
#tradeanalyze(infile)


def doAnalyze(inputDir,fn,outputDir):
    template = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <HTML lang="ja">
      <head>
        <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <META http-equiv="Content-Style-Type" content="text/css">
        <LINK REV="MADE" HREF="mailto:xyz@hoge.com">
        <LINK rel="INDEX" href="./index.html"> 
        <title>$$TITLE$$</title>
        <style type="text/css" media="screen">
        <!--
        td { font: 9pt Tahoma,Arial; }
        -->
        </style>
        <style type="text/css" media="print">
        <!--
        td { font: 7pt Tahoma,Arial; }
        -->
        </style>
        <style type="text/css">
        <!--
        .msdate { mso-number-format:"General Date"; }
        .mspt   { mso-number-format:\#\,\#\#0\.00;  }
        -->
        </style>
    
        <style type="text/css">
        <!--
            div.cent { 
                text-align: center; 
            }
        //-->
        </style>
    
        <style type="text/css">  
        <!-- 
        table.table0 {
           align: center;
           table-layout: auto;
           width: 820px;
           border: 0px; 
        }
        table.table0 td:nth-of-type(1) {
           text-align: left;
           font: 20pt Tahoma,Arial;
        }
        table.table0 td:nth-of-type(2) {
           text-align: center;
           font: 14pt Tahoma,Arial;
        }
        table.table0 td:nth-of-type(3) {
           text-align: right;
           font: 12pt Tahoma,Arial;
        }
        -->
      
        </style>  
        <style type="text/css">  
        <!-- 
        table.table1 {
           align: center;
           width: 820px;
           text-align: center;  
           table-layout: auto;     
           border-collapse: collapse; 
           border: 1px solid gray;   
        }
        table.table1 td:nth-of-type(1) {
           border: 1px solid gray; 
           padding: 3px;            
           text-align: left;
        }    
        table.table1 td:nth-of-type(2) {
           border: 1px solid gray; 
           padding: 3px;           
           text-align: left;
        }    
        -->  
        </style>  
        <style type="text/css">  
        <!-- 
        .table2 {
           align: center;
           width: 820px;
           table-layout: auto;     
           border-collapse: collapse; 
           border: 1px solid gray;   
           height: 8;
           background-color: #FFFFFF;
        }
        .table2 td:nth-of-type(2n+1) {
           border: 1px solid gray; 
           padding: 3px;           
           text-align: left;
           background-color: #E0E0E0;
            }
        .table2 td:nth-of-type(2n) {
           border: 1px solid gray; 
           padding: 3px;           
           text-align: right;
            }    
        -->  
        </style>  
        <style type="text/css">  
        <!-- 
        .table3 {
           table-layout: fixed;
           width: 820px;
           border-collapse: collapse; 
           border: 1px solid gray;   
           background-color: #FFFFFF;
            }
        .table3 td:nth-of-type(1) {
           width: 80px;
           vertical-align:top;
           border: 1px solid gray; 
           padding: 3px;           
           text-align: left;
           background-color: #E0E0E0;
            }
        .table3 td:nth-of-type(2) {
           width: 140px;
           vertical-align:top;
           border: 1px solid gray; 
           padding: 3px;           
           text-align: center;
            }
        .table3 td:nth-of-type(3) {
           vertical-align:center;
           border: 1px solid gray; 
           padding: 3px;           
           text-align: left;
            }
        -->  
        </style>  
    </head>
    
    <!-- $$START_BODY$$ -->
    <body>
    
    <table summary="Title" class="table0">
    <tr>
        <td>$$EANAME$$</td>
        <td>$$TIMEFRAME$$</td>
        <td>$$SIMPERIOD$$</td>
    </tr>
    </table>
    
    <table summary="Summary" class="table1">
    <tr>
        <td>$$EAPARAM$$</td>
    </tr>
    <tr>
        <td><A href="$$HTMLFILE$$">$$HTMLFILE$$</A></td>
    </tr>
    </table>
    <table summary="Summary" class="table2">
    <tr align=left>
        <td>通貨</td>
        <td>$$SYMBOL$$</td>
        <td>Period</td>
        <td>$$PERIOD$$</td>
        <td>総取引</td>
        <td>$$TOTALTRADE$$</td>
        <td>PF</td>
        <td>$$PF$$</td>
        <td>DD(%)</td>
        <td>$$DD$$</td>
    </tr>
    <tr align=left>
        <td>勝率(%)</td>
        <td>$$WINRATE$$</td>
        <td>Long勝率(%)</td>
        <td>$$LONGWINRATE$$</td>
        <td>Short勝率(%)</td>
        <td>$$SHORTWINRATE$$</td>
        <td>連勝</td>
        <td>$$CONSECTIVEWINS$$</td>
        <td>連敗</td>
        <td>$$CONSECTIVELOSSES$$</td>
    </tr>
    </table>
    <img src="$$000001$$"   alt="$$000001$$">
    
    
    <table summary="summary" class="table3">
    <tr>
        <td>Total trades</td><td>$$T001001$$</td>
        <td ><img src="$$I001001$$" alt="$$I001001$$"></td>
    </tr>
    <tr> 
        <td>Long  trades</td><td>$$T001002$$</td> 
        <td ><img src="$$I001002$$" alt="Graph"></td>
    </tr>
    <tr>
        <td>Short trades</td><td>$$T001003$$</td>
        <td ><img src="$$I001003$$" alt="Graph"></td>
    </tr>
    <tr>
        <td>Long  profit rate</td><td>$$T001004$$</td>
        <td rowspan="2"><img src="$$I002001$$"  alt="$$I002001$$"></td>
    </tr>
    <tr>
        <td>Short profit rate</td><td>$$T001005$$</td>
    </tr>
    </table>
    
    <table summary="summary" class="table3">
    <tr> 
        <td>Hour</td><td>profit rate[win/total]</td>
        <td rowspan="25"><img src="$$I003001$$" alt="$$I003001$$"></td>
    </tr>
    <tr> 
        <td>0 H</td><td>$$T002001$$</td>
    <tr> 
        <td>1 H</td><td>$$T002002$$</td>
    </tr>
    <tr> 
        <td>2 H</td><td>$$T002003$$</td>
    </tr>
    <tr> 
        <td>3 H</td><td>$$T002004$$</td>
    </tr>
    <tr> 
        <td>4 H</td><td>$$T002005$$</td>
    </tr>
    <tr> 
        <td>5 H</td><td>$$T002006$$</td>
    </tr>
    <tr> 
        <td>6 H</td><td>$$T002007$$</td>
    </tr>
    <tr> 
        <td>7 H</td><td>$$T002008$$</td>
    </tr>
    <tr> 
        <td>8 H</td><td>$$T002009$$</td>
    </tr>
    <tr> 
        <td>9 H</td><td>$$T002010$$</td>
    </tr>
    <tr> 
        <td>10 H</td><td>$$T002011$$</td>
    </tr>
    <tr> 
        <td>11 H</td><td>$$T002012$$</td>
    </tr>
    <tr> 
        <td>12 H</td><td>$$T002013$$</td>
    </tr>
    <tr> 
        <td>13 H</td><td>$$T002014$$</td>
    </tr>
    <tr> 
        <td>14 H</td><td>$$T002015$$</td>
    </tr>
    <tr> 
        <td>15 H</td><td>$$T002016$$</td>
    </tr>
    <tr> 
        <td>16 H</td><td>$$T002017$$</td>
    </tr>
    <tr> 
        <td>17 H</td><td>$$T002018$$</td>
    </tr>
    <tr> 
        <td>18 H</td><td>$$T002019$$</td>
    </tr>
    <tr> 
        <td>19 H</td><td>$$T002020$$</td>
    </tr>
    <tr> 
        <td>20 H</td><td>$$T002021$$</td>
    </tr>
    <tr> 
        <td>21 H</td><td>$$T002022$$</td>
    </tr>
    <tr> 
        <td>22 H</td><td>$$T002023$$</td>
    </tr>
    <tr> 
        <td>23 H</td><td>$$T002024$$</td>
    </tr>
    </table>
    
    <table summary="summary" class="table3">
    <tr> 
        <td>Weekday</td><td>profit rate[win/total]</td>
        <td rowspan="7"><img src="$$I003002$$" alt="$$I003002$$"></td>
    </tr>
    <tr> 
        <td>mon</td><td>$$T003001$$</td> 
    </tr>
    <tr> 
        <td>tue</td><td>$$T003002$$</td> 
    </tr>
    <tr> 
        <td>wed</td><td>$$T003003$$</td> 
    </tr>
    <tr> 
        <td>thu</td><td>$$T003004$$</td> 
    </tr>
    <tr> 
        <td>fri</td><td>$$T003005$$</td> 
    </tr>
    <tr> 
        <td>sun</td><td>$$T003006$$</td> 
    </tr>
    </table>
    
    
    <table summary="summary" class="table3">
    <tr> 
        <td>Entry - Exit</td><td> profit rate [win/total]</td>
        <td rowspan="7"><img src="$$I004001$$" alt="$$I004001$$"></td>
    </tr>
    <tr> 
        <td>"Long - close"</td><td>$$T004001$$</td>
         
    </tr>
    <tr> 
        <td>"Long -   t/p"</td><td>$$T004002$$</td> 
    </tr>
    <tr> 
        <td>"Long -   s/l"</td><td>$$T004003$$</td> 
    </tr>
    <tr> 
        <td>"Short- close"</td><td>$$T004004$$</td> 
    </tr>
    <tr> 
        <td>"Short-   t/p"</td><td>$$T004005$$</td> 
    </tr>
    <tr> 
        <td>"Short-   s/l"</td><td>$$T004006$$</td> 
    </tr>
    </table>
    
    <table  summary="summary" class="table3">
    <tr> 
        <td>Exit</td><td>rate [count/total]</td>
        <td rowspan="4"><img src="$$I004002$$" alt="$$I004002$$"></td>
    </tr>
    <tr> 
        <td>Close</td><td>$$T005001$$</td> 
    </tr>
    <tr> 
        <td>t/p</td><td>$$T005002$$</td> 
    </tr>
    <tr> 
        <td>s/l</td><td>$$T005003$$</td> 
    </tr>
    </table>
    
    </body>
    </html>
    <!-- $$END_BODY$$ -->
    
    
    """
    import   logging
    logging.basicConfig(filename='analizeReport.log',\
        format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
    print "\n\n=================================================="
    infile = inputDir + fn    
    print " Inputfile =", infile
    try:
        f = cdc.open(infile,'rb','cp932')
    except IOError:
        logging.error("Cannot open " + infile)
        sys.exit("\n Cannot open :"+infile)
    html = f.read()
    f.close()    

    rpt = MT4TestReport()
    try:            
        rpt.feed(html)
    except TypeError:
        print "*** Error Cannot convert " + infile
        logging.warning("Cannot analyze " + infile)
        return
    fname = fn[:-4]
   
    data = dict()        
    headeranalyze(rpt,fname,outputDir,data)
    tradeanalyze(rpt,fname,outputDir,data)
    tradeanalyze2(rpt,fname,outputDir,data)
    tradeanalyze3(rpt,fname,outputDir,data)
    tradeanalyze4(rpt,fname,outputDir,data)
    outhtm = template        
    for k in data.keys():
        outhtm = outhtm.replace(k,data.get(k))
    #print outhtm
    ofln = outputDir + fname + 'Analyze.htm'
    ofl = open(ofln,'wb')
    ofl.write(outhtm)
    logging.info("Create file " + ofln)
    ofl.close()
    print "Create file\n " + ofln    
    
import getopt
import os
def main(argv):

    inputDir  = 'result/'
    outputDir = 'result/'
    try:    
        opts,args = getopt.getopt(argv,"o:i:")
    except getopt.GetoptError:
        print "Usage:"
        print " [-o outdir -i inputdir] inputfile(s)" 
        sys.exit(1)
    for k,v in opts:
        if k == "-o":
            outputDir = v
            if not outputDir.endswith('/'):
                outputDir.join('/')
        if k == "-i":
            inputDir = v
            if not inputDir.endswith('/'):
                inputDir.join('/')

    print "\n******************\nAnalyzing\n******************"
    if len(args) == 0: 
        for fn in os.listdir(inputDir):
            if fn.endswith(".htm") and fn[0] != '_' and not fn.endswith('Analyze.htm'):
                doAnalyze(inputDir,fn,outputDir)
    
    else:
        for f in args:
            fn = str(f)
            doAnalyze(inputDir,fn,outputDir)            
    

if __name__ == '__main__':
    main(sys.argv[1:])

    
