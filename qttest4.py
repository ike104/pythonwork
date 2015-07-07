# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 09:13:10 2015

@author: ikeda
"""

# -*- coding:utf-8 -*-
 
import sys
import math
from PyQt4 import QtGui as gui
from PyQt4 import QtCore as qt
 
class Hoge(gui.QWidget):
    def __init__(self):
        super(Hoge, self).__init__()
        self.initUi()
 
    def initUi(self):
        grid = gui.QGridLayout()
        self.setLayout(grid)
 
        form = gui.QFormLayout()
        grid.addLayout(form,1,0)
 
        self.cmbCharCd = gui.QComboBox()
        self.cmbCharCd.addItems(('utf-8','shift-jis','euc-jp','utf-16'))
        form.addRow(u"文字コード", self.cmbCharCd)
 
        boxCtrl = gui.QHBoxLayout()
        self.chkFullByte = gui.QCheckBox(u"詳細(Byte)")
        self.chkFullByte.setCheckState(qt.Qt.Unchecked)
        boxCtrl.addWidget(self.chkFullByte)
 
        self.chkCountWs = gui.QCheckBox(u"空白計測")
        self.chkCountWs.setCheckState(qt.Qt.Checked)
        boxCtrl.addWidget(self.chkCountWs)
 
        self.btnConv = gui.QPushButton(u"計測")
        self.btnConv.clicked.connect(self.doCount)
        boxCtrl.addWidget(self.btnConv)
 
        form.addRow(boxCtrl)
 
        self.txtChCnt = gui.QLineEdit()
        self.txtChCnt.setAlignment(qt.Qt.AlignRight)
        self.txtByteCnt = gui.QLineEdit()
        self.txtByteCnt.setAlignment(qt.Qt.AlignRight)
 
        form.addRow(u"文字数", self.txtChCnt)
        form.addRow(u"バイト数", self.txtByteCnt)
 
        boxBtn = gui.QHBoxLayout()
        grid.addLayout(boxBtn,2,0)
 
        self.txtSource = gui.QTextEdit()
        grid.addWidget(self.txtSource, 3, 0)
 
        self.setWindowTitle('CharCounter')
        self.show()
 
    def doCount(self):
 
        uc_text = unicode(self.txtSource.toPlainText())
        encoding = unicode(self.cmbCharCd.currentText())
 
        is_omit_byte = not self.chkFullByte.isChecked()
        is_ignore_ws = not self.chkCountWs.isChecked()
 
        ch_cnt = 0
        byte_len = 0
        for uc_char in uc_text:
 
            if is_ignore_ws and uc_char.isspace():
                continue
 
            byte_len = byte_len + len(bytearray(uc_char, encoding))
            ch_cnt = ch_cnt + 1
 
        self.txtChCnt.setText("{:,}".format(ch_cnt))
        self.txtByteCnt.setText(self.formatByte(byte_len, is_omit_byte))
 
    def formatByte(self, byte_len, is_omit_byte):
        SI_KILO = 1024.0
        SI_PREFIX = ('','KB','MB','GB','TB')
 
        if is_omit_byte:
            lc = math.log(byte_len, SI_KILO)
            byte_omit_len = byte_len
 
            byte_omit_len = byte_omit_len / math.pow(SI_KILO,int(lc))
 
            print unicode(byte_omit_len)
            return "{:.1f}".format(byte_omit_len) + SI_PREFIX[int(lc)]
        else:
            return "{:,}".format(byte_len)
 
def main():
    app = gui.QApplication(sys.argv)
    hoge = Hoge()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()