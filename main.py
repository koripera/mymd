#https://python-markdown.github.io/
#https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41

"""
mdファイルをhtmlファイルに変換して、flaskでの閲覧をさせる

"""
import os
import glob
import re
import platform

from flask import Flask, send_file, Response, abort
import markdown
from waitress import serve

app = Flask(__name__)

cssstyle=("""\
<style>
pre{
background-color: #eee;
padding-left: 20px;
padding-top: 20px;
padding-bottom: 20px;
}

code {
background-color: #eee;
border-radius: 3px;
}

summary {
cursor: pointer;
display: flex;
align-items: center;
list-style: none;
}

summary:before {
	content: '▶'; /* カスタムアイコンを追加 */
	margin-right: 0.5em;
	display: inline-block;
	transform: rotate(0);
	transition: transform 0.3s ease;
}

summary h2 {
	margin: 0; /* 不要な余白を削除 */
	font-size: 1.25em; /* 必要に応じて調整 */
	font-weight: bold;
}

summary::-webkit-details-marker {
	display: none; /* デフォルトの矢印アイコンを非表示にする */
}

details[open] summary:before {
	transform: rotate(90deg); /* アイコンを回転させて開閉を表現 */
}

details {
	margin-bottom: 1em;
	border: 1px solid #ccc;
	border-radius: 5px;
	padding: 0.5em;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

</style>

""")

def fold(html):#<h2></h2>の要素を折りたたみたい
	pattern = "<h2>.*?</h2>"

	txt=""

	#タイトルを取る
	titles = re.findall(pattern,html)

	#各要素内を取得
	for i,content in enumerate(re.split(pattern,html)):
		if i==0:
			txt+=content
		if i!=0:
			if titles[i-1]=="<h2>contents</h2>":
				txt+=f"{titles[i-1]}{content}"
			else:
				txt+=f"<details open><summary><span>{titles[i-1]}</span></summary>{content}</details>"

	return txt
	

@app.route("/")
def index():
	a=""

	for name in glob.iglob("mdfile/**/*.md",recursive=True):
		a += f"<a href='{name[7:][:-3]}' target='_blank'>{name[7:]}</a><br>\n"
	
	#.mdﾌｧｲﾙへのﾘﾝｸを作成する	
	#for name in glob.iglob("mdfile/**/*.md",recursive=True):
	#	a+=f"[{name[7:]}]({name[7:][:-3]})  \n"

	#ﾊﾟｰｻｰの作成とhtmlの組み立て
	#md = markdown.Markdown(extensions=["fenced_code"])
	#md_template = cssstyle+ md.convert(a)

	return a
		

@app.route("/<path:path>")
def output(path):#指定URLの.mdﾌｧｲﾙをhtml化,加工して返す

	filepath=f"mdfile/{path}.md"

	#ﾌｧｲﾙないならｴﾗｰ
	if not os.path.isfile(filepath):
		return abort(404)	

	#指定ﾌｧｲﾙの読み込み
	with open(filepath,'r',encoding="utf-8") as f:
		a = f.read()

	#ﾊﾟｰｻｰの作成とhtmlの組み立て
	md = markdown.Markdown(extensions=["fenced_code"])
	md_template = cssstyle+ md.convert(a)

	return fold(md_template)


if __name__=="__main__":
	os_name = platform.system()
	if os_name == "Windows":os.system('cls')
	else                   :os.system('clear')
	print("mymd")
	print("http://localhost:5000")
	serve(app,port=5000)
	#app.run(debug=True)
