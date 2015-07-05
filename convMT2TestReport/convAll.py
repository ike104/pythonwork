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
  convAll.py  (本ファイル)
  convMT4TestReportHTML2.py
  summary.py
  analyzeReport.py  
  を、MT4のTestReportの.htm,.gifがある場所にコピー
  この場所に、result/フォルダを作成
  
　　実行
　　  convAll.py をダブルクリック
    または、ipython シェルを起動して、
    run conAll env*.htm 
    などのようにワイルドカード指定で起動する。
    または、
    ipython convall.py %1
    のような.batファイルを作成して、そのバッチにhtmファイルを
    ドロップする
    または、convAll.pyにhtmlファイルをドロップする。
    
"""
import os
import sys
import glob
import convMT4TestReportHTML2

#------------------------------------------------------
def main(argv):
    """
    同じディレクトリのhtmlファイルをすべて変換
    """
    outDir = 'result/'
    inpFiles = '*.htm'
    # ドロップファイルした時のカレントディレクトリがwindows/system32などになっているので、
    # スクリプトのあるディレクトリに移動しておく
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    if len(argv)==0:
        iafiles = glob.glob(inpFiles)
    else:
        iafiles = argv
    print "  Found %d files" % (len(iafiles)) 
    ifiles = []    
    for j in iafiles:
        ifiles.append(os.path.basename(j))
    if len(ifiles)<=0:
        print "No file(s) : " + inpFiles
        raw_input()
        sys.exit(0)
    pfiles  = []
    for fname in ifiles:
        f = str('"'+str(fname)+'"')
        pfiles.append(convMT4TestReportHTML2.do_conv(f,outDir))
    
    #------------------------------------------------------
    import summary
    print 'OutputDirectory: ' + str(outDir)
    summary.main([outDir])
    
    #print "\n*** pfiles ***\n"    
    #print pfiles    
    import analyzeReport
    for f in pfiles:
        print f        
        analyzeReport.main(["-o",outDir,"-i",f[1],f[0]+".htm"])


if __name__ == '__main__':
    main(sys.argv[1:])
