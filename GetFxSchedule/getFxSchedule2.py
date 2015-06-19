# -*- coding: cp932 -*-
import csv
from HTMLParser import HTMLParser

class ForexCalenderGetterFF(HTMLParser):
    """My HTMLParser for FOREX Factory Calender"""


    def __init__(self,year):
        self.year = year
        self.state=0
        self.count=0
        self.itemcount=0
        self.curatr=''
        self.result = []
        self.lineDict = {}
        self.csvField = ['index','data-eventid','date','time','currency','event','impact','previous','forecast','actual']
        self.curDate = ''
        self.curTime = ''
        self.dictData = []
        HTMLParser.__init__(self)

    def _line_out(self):
        if len(self.lineDict) > 0:
            self.lineDict['index'] = self.itemcount
            self.itemcount = self.itemcount+1
            if 'date' not in self.lineDict:
                self.lineDict['date'] = self.curDate
            if 'time' not in self.lineDict:
                self.lineDict['time'] = self.curTime
            try:
                if parse(self.lineDict['date']).year != self.year:
                    self.lineDict['date'] = self.lineDict['date'] + ' ' + str(self.year)
            except ValueError:
                pass
            #print self.lineDict
            self.dictData.append(self.lineDict)
            self.lineDict = {}

    def handle_starttag(self, tag, attrs):
        if self.state==2:
             if tag=='td' or tag=='tr' or  tag=='span':
                 if len(attrs)>1 and attrs[0][1] == 'impact':
                     pass
                 elif len(attrs)>1 and attrs[0][0] == 'title':
                     self.curatr = [('impact',attrs[1][1])]
                     #print self.curatr
                 else:
                     if len(attrs)>0:
                         self.curatr = attrs
                     if len(attrs) == 2 and attrs[1][0]=='data-eventid':
                         self._line_out()

                 #print("start tag:", tag, attrs)
        else:
            if tag == 'thead':
                self.state=1 # found table header block !
    def handle_endtag(self, tag):
        if self.state == 2:
            if tag=='td':
                pass
                #print("end tag :", tag)
            if tag == 'table':
                self._line_out()
                self.state = 10 # End of "table" is end of data block
                #self.csvFile.close()
        else:
            if tag == 'thead' and self.state ==1:
               self.state = 2 # found table header block and start to get
    def handle_data(self, data):
        if self.state == 2:
            data = data.rstrip().lstrip()
            #print("data  :", data)
            self.count = self.count + 1
            #self.result.append(self.itemcount,self.count,self.curatr,data)
            #print self.itemcount, self.count, self.curatr, data
            if len(self.curatr) == 2 and self.curatr[1][0] == 'data-eventid':
                fieldname = self.curatr[1][0]
                data = self.curatr[1][1]
                self.lineDict[fieldname] = data
            elif len(self.curatr)==1:
                if len(data) >= 1:
                    fieldname = self.curatr[0][1]
                    self.lineDict[fieldname] = data
                    if fieldname == 'date':
                        self.curDate = data + ' ' + str(self.year)
                    if fieldname == 'time':
                        self.curTime = data
                else:
                    if self.curatr[0][0]=='impact':
                        self.lineDict['impact']=self.curatr[0][1]
html =  ('<html><tr><table><thead></thead>'
'<tr class="borderfix"><td></td></tr>'
'<tr class="calendar_row newday" data-eventid="57824">'
'<td class="date"><span class="date">Mon<span>Jun 1</span></span></td>'
'<td class="time">21:30</td> <td class="currency">USD</td>'
'<td class="impact"> <span title="Medium Impact Expected" class="medium">'
'</span> </td> <td class="event"><span>Core PCE Price Index m/m</span></td>'
'<td class="detail"><a class="calendar_detail level1" data-level="1"></a></td>'
'<td class="actual"> <span class="worse">0.1%</span> </td>'
'<td class="forecast">0.2%</td> <td class="previous">0.1%</td>'
'<td class="graph"><a class="calendar_chart"></a></td> </tr> '
'</tr></html>')

from dateutil.parser import parse
import datetime
import time
class MyFxCalenderFormatter():
    """ My Special FX calender formatter """
    
    def __init__(self):
        self.timediff = 13 # FFのChallenderは大西洋標準時(UTC-4)を基準にしているこれをJST（UTC+9)に変換する
        self.field = ['flag_','date_time','currency_name','impact_level','event_name']
        self.impacttable = { 'high':5, 'medium':3, 'low':1}
        self.result = []
    def feed(self,dic):
        self.result = []
        if not dic.has_key('data-eventid'):
            return
        if not dic.has_key('currency'):
            return
        if not dic.has_key('event'):
            return
        if dic.has_key('date') and dic.has_key('time'):
            dt = dic['date'] + ' ' + dic['time']
            #print dt
            try:
                d = parse(dt) + datetime.timedelta(hours =  self.timediff )
                dtime = d.strftime("%Y.%m.%d %H:%M")
            except ValueError:
                dtime = ''
        else:
            dtime=''
        try:
            imp = self.impacttable[dic['impact']]
        except KeyError:
            imp = 0
        if imp>0 and len(dtime)>0:
            flg = 1
        else:
            flg = 0
        self.result = {self.field[0]:flg, self.field[1]:dtime,self.field[2]:dic['currency'],self.field[3]:imp, self.field[4]:dic['event']}
        self.result.update(dic)
        
import urllib2
            
class MyFxCalenderGetter():
    """Get FX callendar from specified URL and output CSV file"""

    def __init__(self,url,csv,year):
        self.url = url
        self.csv = csv
        self.year = year
    def fetch(self):
        response = urllib2.urlopen(self.url)
        html = response.read()
        response.close()

        parser = ForexCalenderGetterFF(self.year)
        parser.feed(html)
        parser.close()
        dic = parser.dictData
        field = parser.csvField
        csvFile = open(self.csv, 'wb')
        cnv = MyFxCalenderFormatter()
        fieldorg = cnv.field
        csvWriter = csv.DictWriter(csvFile, fieldorg + field,restval=' ',extrasaction='ignore')
        for i in range(0,len(dic),1):
            cnv.feed(dic[i])
            dic2 = cnv.result
            if len(dic2)>0:
                ##print dic[i]
                csvWriter.writerow(dic2)
        csvFile.close()
        print 'Fetched', parser.itemcount, 'items'
#
# 
#
def doFetch(year, mon):
    """Do Fetch Monthly schedule """

    
    #url = 'http://www.forexfactory.com/calendar.php?month=jan.2015'
    #csvFileName = 'csvtst.txt'
    urlbase = 'http://www.forexfactory.com/calendar.php?month='
    csvbase = 'FxCal'
    csvext  = '.txt'

    url = urlbase + datetime.date(year,mon,1).strftime("%b.%Y").lower()
    print 'URL=',url
    csvFileName = csvbase + datetime.date(year,mon,1).strftime("%Y%m") + csvext
    print 'CSV=',csvFileName
    getter = MyFxCalenderGetter(url,csvFileName,year)
    getter.fetch()


def getYearMonth(backweeks,forwardweek):
    """ return (year,month) back/forward from now """ 

    st = datetime.date.today()-datetime.timedelta(weeks=backweeks)
    year,month = st.year,st.month
    #print year, month

    et = datetime.date.today()+datetime.timedelta(weeks=forwardweeks)
    eyear,emonth = et.year,et.month
    #print eyear,emonth
    deltamonth = eyear*12+emonth - year*12-month+1

    span = []
    for i in range(0,deltamonth,1):
        #print year,month
        a = (year,month)
        span.append(a)
        month = month+1
        if month>12:
            month = 1
            year = year+1
    return span    


#------ これを開いてRun(F5)するとFOREX FACTORYのカレンダーにアクセスして、イベントのCSVファイルを作成する。    

backweeks=300 ## さかのぼる週
forwardweeks = 3 ## 先の週

s=getYearMonth(backweeks,forwardweeks)
print 'Calc. span is',s
for t in s:
    doFetch(t[0],t[1])







