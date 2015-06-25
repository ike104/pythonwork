from xml.etree.ElementTree import *

#<window width="1920">
#	<title font="large" color="red">sample</title>
#	<buttonbox>
#		<button>OK</button>
#		<button>Cancel</button>
#	</buttonbox>
#</window>
# 文字列から作成
xmlString = '<window width="1920"><title font="large" color="red">sample</title><buttonbox><button>OK</button><button>Cancel</button></buttonbox></window>'
elem = fromstring(xmlString) # ルート要素を取得(Element型)

#ファイルから作成
#tree = parse("sample.xml") # 返値はElementTree型
#elem = tree.getroot() # ルート要素を取得(Element型)


