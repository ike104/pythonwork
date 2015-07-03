# coding=Shift_JIS

#txt����html�𐶐�����
#�P�s�ڂ��^�C�g���A
#�Q�s�ڂ��y�[�W�ڍ�
#�O���t�@�C���}��: ��filename
#���o���Q: ��text
#���o���R: �{text
#���s�Ȃ��F��text�@�i�e�[�u�����L�q�������Ƃ��Ȃǁj

import re
import glob
import string
from xml.sax.saxutils import escape

FILE_HEADER = "define/header.txt"
FILE_TITLE = "define/title.txt"
FILE_FOOTER = "define/footer.txt"



#���[�e�B���e�B
def indent(instr):
    #���͕�������C���f���g
    ret = ""
    for line in instr.split('\n'):
        ret += "\t" + line + "\n"
    return ret.rstrip('\n')

#�O���\�[�X�R�[�h�̑}��
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


#���v�f�^�O
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
            if(line[0:2]=="��"):
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
        Wiki���\���f�[�^�t�@�C������
        html������𐶐����ĕԂ�
        '''

        #���^��������A��������N���X���`
        midasi = {"��":H2, "�{":H3, "��":SourceCode}

        outPage = Page()
        divbody = Div()
        dan = Danraku()

        for line in lines:
            rawtext = line.strip("\n")

            command = line[0:2]
            #���o��
            if(command in midasi):
                outPage.addElement(divbody)
                divbody = Div()

                elementClass = midasi[command]
                rawtext = rawtext[2:]
                outPage.addElement(elementClass(rawtext))
                continue

            #��s
            if(rawtext == ""):
                divbody.addElement(dan)
                dan = Danraku()
                continue

            dan.addLine(rawtext)
        #�Ō�Ɏc�����i����ǉ�
        divbody.addElement(dan)
        outPage.addElement(divbody)
        return outPage.toString()

#�������珈���J�n
print("*** HTML�R���o�[�^ ***")
txtlist = glob.glob("*.txt")
for infile in txtlist:
    html = re.sub(".txt", ".html", infile)
    f = open(infile)
    lines = f.readlines()
    page = PageConverter()

    #�P�A�Q�s�ڂ̓^�C�g���ƏڍׂɎg��
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
    print("\t" + "�ϊ�����")
print("�������������܂����B")

