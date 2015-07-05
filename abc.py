# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 08:54:03 2015

@author: ikechan
"""

# do_drag_and_drop.py
import sys
import glob

def main(argv):
    """
    この　スクリプトファイルにファイルをドロップできる
    """
    inpFiles = '*.htm'
    if len(argv)==0:
        ifiles = glob.glob(inpFiles)
    else:
        ifiles = argv
    print "  Found %d files" % (len(ifiles)) 
    if len(ifiles)<=0:
        print "No file(s) : " + inpFiles
        sys.exit(0)
    
    for n in ifiles:
        print n
    raw_input()
    
if __name__ == '__main__':
    main(sys.argv[1:])
