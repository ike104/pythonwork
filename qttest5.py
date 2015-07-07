# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 09:41:17 2015

@author: ikeda
"""
import sys
import os, types
from PyQt4 import QtCore, QtGui, uic

class MyQtGuiMeta(QtCore.pyqtWrapperType):
    @staticmethod
    def should_rebuild(uifile, pyfile):
        return not os.path.isfile(pyfile) or (
            os.path.isfile(uifile) and \
            (os.path.getmtime(pyfile) < os.path.getmtime(uifile))
        )

    def __new__(cls, name, bases, attr):
        # ここで.uiファイルを作成して読み込む
        _path = os.path.dirname(__file__)
        uifile = os.path.join(_path, attr["_uifile"])
        pyfile = uifile.replace(".ui", "_ui.py")
        if cls.should_rebuild(uifile, pyfile):
            # .uiファイルの方が新しければ_ui.pyファイルを作成
            uic.compileUi(uifile, open(pyfile, "w"))
        try:
            # モジュールとして読み込む
            modname = os.path.splitext(os.path.basename(uifile))[0] + "_ui"
            modname = "qt4.%s" % modname
            mod = __import__(modname, fromlist=["*"])
            classnames = [x for x in dir(mod) if x.startswith("Ui_")]
            if len(classnames) != 1:
                raise ValueError("Can't determine ui class to use in %s" % modname)
            ui_class = getattr(mod, classnames[0])
        except ImportError:
            ui_class, base_class = uic.loadUiType(uifile)
        # ベースクラスにセット
        bases += (ui_class,)
        return QtCore.pyqtWrapperType.__new__(cls, name, bases, attr)

class MyMainWindow(QtGui.QMainWindow):
    __metaclass__ = MyQtGuiMeta
    _uifile = "qt.ui"
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wnd = MyMainWindow()
    wnd.show()
    sys.exit(app.exec_())