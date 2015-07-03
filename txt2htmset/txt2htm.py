# coding=Shift_JIS

#txtからhtmlを生成する
#１行目がタイトル、
#２行目がページ詳細
#外部ファイル挿入: ％filename
#見出し２: ■text
#見出し３: ＋text
#改行なし：＠text　（テーブルを記述したいときなど）

import re
import glob
import string
from xml.sax.saxutils import escape

FILE_HEADER = "define/header.txt"
FILE_TITLE = "define/title.txt"
FILE_FOOTER = "define/footer.txt"



#ユーティリティ
def indent(instr):
    #入力文字列をインデント
    ret = ""
    for line in instr.split('\n'):
        ret += "\t" + line + "\n"
    return ret.rstrip('\n')

#外部ソースコードの挿入
def insertCode(sourcefile):
    outlist = []
    f = open(sourcefile)
    code = f.readlines()
    outlist.append('<textarea cols="50" rows="5" style="width:400px;height:300px;font-size:10pt">')
    for line in code:
        outlist.append(escape(line))

    outlist.append('</textarea>')
    f.close()
    return string.join(outlist,"")


#非空要素タグ
class Tag:
    def __init__(self, value):
        self.value = value

class H2(Tag):
    def toString(self):
        return "<h2>" + self.value + "</h2>"

class H3(Tag):
    def toString(self):
        return "<h3>" + self.value + "</h3>"

class Danraku():
    def __init__(self):
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)

    def toString(self):
        if(len(self.lines)==0):
            return ""

        value = '<p style="margin: 5px 5px 5px 0px;">\n'
        for index,line in enumerate(self.lines):
            if(line[0:2]=="＠"):
                value += "\t" + line[2:] + "\n"
                continue

            value += "\t" + line
            if index < len(self.lines)-1:
                value += "<br />"
            value += "\n"
        value += "</p>"
        return value


class SourceCode(Tag):
    def toString(self):
        scriptfile = self.value
        retstr = insertCode(scriptfile)
        return retstr

class Page:
    def __init__(self):
        self.elements = []

    def addElement(self, element):
        self.elements.append(element)

    def toString(self):
        value = ""
        for element in self.elements:
            value += element.toString() + "\n"
        return value

class Div(Page):

    def toString(self):
        if(len(self.elements)==0):
            return ""

        if(len(self.elements)==1):
            if(self.elements[0].toString()==""):
                return ""


        value = '<div class="bodytext" style="padding: 12px; align: justify">\n'
        for element in self.elements:
            value += indent(element.toString()) + "\n"
        value += "</div>"
        return value

class PageConverter:
    def getheader(self):
        return open(FILE_HEADER).read()

    def gettitleblock(self):
        return open(FILE_TITLE).read()

    def getfooter(self):
        return open(FILE_FOOTER).read()

    def convert(self, lines):
        '''
        Wiki風構文データファイルから
        html文字列を生成して返す
        '''

        #メタ文字から、生成するクラスを定義
        midasi = {"■":H2, "＋":H3, "％":SourceCode}

        outPage = Page()
        divbody = Div()
        dan = Danraku()

        for line in lines:
            rawtext = line.strip("\n")

            command = line[0:2]
            #見出し
            if(command in midasi):
                outPage.addElement(divbody)
                divbody = Div()

                elementClass = midasi[command]
                rawtext = rawtext[2:]
                outPage.addElement(elementClass(rawtext))
                continue

            #空行
            if(rawtext == ""):
                divbody.addElement(dan)
                dan = Danraku()
                continue

            dan.addLine(rawtext)
        #最後に残った段落を追加
        divbody.addElement(dan)
        outPage.addElement(divbody)
        return outPage.toString()

#ここから処理開始
print("*** HTMLコンバータ ***")
txtlist = glob.glob("*.txt")
for infile in txtlist:
    html = re.sub(".txt", ".html", infile)
    f = open(infile)
    lines = f.readlines()
    page = PageConverter()

    #１、２行目はタイトルと詳細に使う
    title = lines[0]
    desc = lines[1]

    outstr = ""
    outstr += page.getheader()
    outstr += page.gettitleblock()
    outstr += page.convert(lines[2:])
    outstr += page.getfooter()

    outstr = re.sub("%title%", title, outstr)
    outstr = re.sub("%desc%", desc, outstr)


    f = open(html,"w")
    f.write(outstr)
    f.close()
    print("\t" + infile + " -> " + html)
    print("\t" + "変換完了")
print("処理が完了しました。")

