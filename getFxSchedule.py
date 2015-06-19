import csv
from HTMLParser import HTMLParser

class ForexCalenderGetterFF(HTMLParser):
    """My HTMLParser for FOREX Factory Calender"""

    
    def __init__(self):
        self.state=0
        self.count=0
        self.itemcount=0
        self.curatr=''
        self.result = []
        self.lineDict = {}
        self.csvField = ['index','data-eventid','date','time','currency','event','impact','previous','forecast','actual']
        self.curDate = ''
        self.dictData = []
        HTMLParser.__init__(self)

    def _line_out(self):
        if len(self.lineDict) > 0:
            self.lineDict['index'] = self.itemcount   
            self.itemcount = self.itemcount+1
            if 'date' not in self.lineDict:
                self.lineDict['date'] = self.curDate
            #print self.lineDict
            self.dictData.append(self.lineDict)
            self.lineDict = {}
                
    def handle_starttag(self, tag, attrs):
        if self.state==2:
             if tag=='td' or tag=='tr' or  tag=='span':
                 if len(attrs)>1 and attrs[0][1] == 'impact':
                     pass
                 elif len(attrs)>1 and attrs[0][1] == 'title':
                     self.curatr = attrs   
                 else:
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
            print("data  :", data)
            self.count = self.count + 1
            #self.result.append(self.itemcount,self.count,self.curatr,data)
            data = data.rstrip().lstrip()
            print self.itemcount, self.count, self.curatr, data
            if len(self.curatr) == 2 and self.curatr[1][0] == 'data-eventid':
                fieldname = self.curatr[1][0]
                data = self.curatr[1][1]
                self.lineDict[fieldname] = data
            elif len(self.curatr)==1 and len(data) > 1:
                fieldname = self.curatr[0][1]
                self.lineDict[fieldname] = data
                if fieldname == 'date':
                    self.curDate = data
                if fieldname == 'impact':
                    self.lineDict[fieldname] = self.curatr[0][1]

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

url = 'http://www.forexfactory.com/calendar.php?month=this'
import urllib2
response = urllib2.urlopen(url)
html = response.read()
response.close()

parser = ForexCalenderGetterFF()
parser.feed(html)
parser.close()
dic = parser.dictData
field = parser.csvField

csvFileName = 'csvtst.txt'
csvFile = open(csvFileName, 'wb')
csvWriter = csv.DictWriter(csvFile, field,restval=' ',extrasaction='ignore')
for i in range(0,len(dic),1):
    ##print dic[i]
    csvWriter.writerow(dic[i])
csvFile.close()    

      
    
