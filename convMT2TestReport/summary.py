# -*- coding: utf-8 -*-
"""
Created on Sat Jul 04 23:27:26 2015

@author: ikechan
"""

#------------------------------------------------------

import os
def main(argv): 
    """
    出力ディレクトリの個別summary(.txt)ファイルを集めて、１つのsummary(.csv)
    ファイルを作成する
    """
    print "argv" + str(argv)    
    outDir = 'result/'    
    if len(argv)>=1:
      outDir = argv[0]      
    
    print '\n***************\nMaking summary\n***************'    
    rows = []
    for fn in os.listdir(outDir):
        if fn.endswith(".txt"):
            f = str(outDir+fn)
            print "Read txt file ="+ f        
            fi = open(f,'r')        
            line = fi.readlines()
            rows.append(line[1])
            fi.close()
    head = line[0]
    head = head.replace('\t',',')
     
    path = os.getcwd() + '\\' + outDir       
    sumfname = outDir+"_summary.csv"
    sumfile = open(sumfname,"w")
    sumfile.write(head)
    for d in rows:
        # htmファイルはハイパーリンクにする    
        dd = d.split('\t')
        if dd[14][len(dd[14])-1]=='\n':
            dd[14] = dd[14][0:len(dd[14])-1]
        dd[14] = '=HYPERLINK("file://' + path+dd[14]
        dd[14] = dd[14] + '")'
        #print dd[14]    
        s = ''    
        for k in dd:
            s = s + k + ','
        s = s[0:len(s)-1]
        if s.find('\n') > 0:
            s = s[0:s.find('\n')-1]
        sumfile.write(s+'\n')
    sumfile.close()
    
    print "\nCreated: summary csv file  "
    print sumfname
    
    templateHtm = \
    """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html>
      <head>
      <meta http-equiv="Content-Type" 
                content="text/html; charset=UTF-8">
        <title>$$TITLE$$</title>
        <style type="text/css" media="screen">
        <!--
        td { font: 9pt Tahoma,Arial; }
        //-->
        </style>
        <style type="text/css" media="print">
        <!--
        td { font: 7pt Tahoma,Arial; }
        //-->
        </style>
        <style type="text/css">
        <!--
        .msdate { mso-number-format:"General Date"; }
        .mspt   { mso-number-format:\#\,\#\#0\.00;  }
        //-->
        </style>
    	
    	<style type="text/css">  
    	<!-- 
    	table.table0 {
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
      </head>
    
    <!--- $$START_BODY$$ --->
    <body topmargin=1 marginheight=1>
    <div align=center>
    
    <table class="table0">
    <tr>
    	<td>$$EANAME$$</td>
    	<td>$$TIMEFRAME$$</td>
    	<td>$$SIMPERIOD$$</td>
    </tr>
    </table>
    
    <table class="table1">
    <tr>
    	<td>$$EAPARAM$$</td>
    </tr>
    <tr>
    	<td><A href="$$HTMLFILE$$">$$HTMLFILE$$</A></td>
    </tr>
    <tr>
    	<td><A href="$$HTMLFILEANA$$">$$HTMLFILEANA$$</A></td>
    </tr>
    </table>
    <table class="table2">
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
    <img src="$$TRADEIMAGE$$" width=820 height=200 border=0 alt="Graph">
    </body>
    <!--- $$END_BODY$$ --->
    
    """
    
    """
     個別サマリーファイル(.txt)を検索して、全体サマリーhtmファイルを作成する。
     
    """
    titlemark = '$$TITLE$$'
    startmark = '$$START_BODY$$'
    endmark = '$$END_BODY$$'
    
    #tmplatefname = '_templateUTF8.tpl'
    
    rows = []
    for file in os.listdir(outDir):
        if file.endswith(".txt"):
            f = str(outDir+file)
            #print f        
            fi = open(f,'r')        
            line = fi.readlines()
            rows.append(line[1])
    head = line[0]
    head = head.replace('\t',',')
    
    #tplfile = open(tmplatefname,'r')
    #tpl = tplfile.read()
    #tplfile.close()
    tpl = templateHtm
     
    block = tpl.split(startmark)
    head = block[0][0:block[0].rfind('<')-1]
    bodytpl = block[1][block[1].find('>')+1:block[1].find(endmark)-6]
    
    summryhtmfname = outDir + '_summary.htm'
    summryhtm = open(summryhtmfname,'wb')
    
    head = head.replace(titlemark,'EA Backtest summary')
    summryhtm.write(head)
    
    for d in rows:
        # htmファイルはハイパーリンクにする    
        dd = d.split('\t')
        body = bodytpl.replace('$$SYMBOL$$',dd[0])
        body = body.replace('$$TIMEFRAME$$',dd[1])
        body = body.replace('$$PERIOD$$',dd[1])
        body = body.replace('$$EANAME$$',dd[3])
        body = body.replace('$$SIMPERIOD$$',dd[4]+' - '+dd[5])
        body = body.replace('$$TOTALTRADE$$',dd[6])
        body = body.replace('$$PF$$',dd[7])
        body = body.replace('$$DD$$',dd[8])
        body = body.replace('$$WINRATE$$',dd[9])
        body = body.replace('$$SHORTWINRATE$$',dd[10])
        body = body.replace('$$LONGWINRATE$$',dd[11])
        body = body.replace('$$CONSECTIVEWINS$$',dd[12])
        body = body.replace('$$CONSECTIVELOSSES$$',dd[13])
        htmlnk=dd[14]
        if htmlnk[len(htmlnk)-1]=='\n':
            htmlnk = htmlnk[0:len(htmlnk)-1]
        giffname = htmlnk.replace('.htm','.gif')
        body = body.replace('$$TRADEIMAGE$$',giffname)
        body = body.replace('$$HTMLFILE$$',htmlnk)
        body = body.replace('$$HTMLFILEANA$$',htmlnk.replace('.htm','Analyze.htm'))
        body = body.replace('$$EAPARAM$$',dd[15])
        
        summryhtm.write(body)
    summryhtm.close()
    print '\nCreated: total summary htm file'
    print str(summryhtmfname)

import sys
if __name__ == '__main__':
    main(sys.argv[1:])

    

