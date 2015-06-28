# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:17:38 2015

@author: ikechan

 同じディレクトリにおかれたMT4の.htmリポートファイルをすべて
　　１）リポートの内容に応じた.htmファイル名に変更（.gifも含めて）
  ２）個別サマリ(.txt)を作成
  ３）個別パラメータファイル(.set)を作成
  　　ここまでは、convMT4TestReportHTML2.pyが行う
　 4)個別サマリから、集約サマリ(.csv)(.htm)を作成
  
 ・ 出力ファイルは、result/フォルダに出力されるので、あらかじめ作成しておくこと。
　・　個別サマリ（.txt）は、クリップボードからexcelなどへのペーストを考慮して,タブ区切り
　・　セットファイルは、テストを実運用したり再試験時の利便性を考えて出力
 ・ 集約サマリ（.csv)はバックテストの結果をソートしたり、比較したりするのに便利
 ・ 集約サマリ（.htm)はバックテストの結果を一覧でブラウズするのに便利
 ・　MT4のTestResultフォルダで運用されることを前提で作成している
 
　インストールに必要なもの
 　convMT4TestReportHTML_all.py  (本ファイル)
  convMT4TestReportHTML2.py
  _templateUTF8.tpl (summary.htmのテンプレート)
  を、MT4のTestReportの.htm,.gifがある場所にコピー
  この場所に、result/フォルダを作成
  
　　実行
　　  convMT4TestReportHTML_all.py　をダブルクリック
    
"""

import os
import convMT4TestReportHTML2

#------------------------------------------------------
"""
同じディレクトリのhtmlファイルをすべて変換
"""
outDir = 'result/'

for file in os.listdir('.'):
    if file.endswith(".htm"):
        f = str('"'+file+'"')
        print f
        convMT4TestReportHTML2.do_conv(f,outDir)
        
        

#------------------------------------------------------
"""
出力ディレクトリの個別summary(.txt)ファイルを集めて、１つのsummary(.csv)
ファイルを作成する
"""

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

print "Created: summary csv file \n "
print sumfname

#------------------------------------------------------
"""
 個別サマリーファイル(.txt)を検索して、全体サマリーhtmファイルを作成する。
 
"""
titlemark = '$$TITLE$$'
startmark = '$$START_BODY$$'
endmark = '$$END_BODY$$'

tmplatefname = '_templateUTF8.tpl'

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

tplfile = open(tmplatefname,'r')
tpl = tplfile.read()
tplfile.close()
 
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
    body = body.replace('$$EAPARAM$$',dd[15])
    
    summryhtm.write(body)
summryhtm.close()
print 'Created: total summary htm file \n '
print str(summryhtmfname)




