"""
mdファイルをhtmlファイルに変換して、flaskでの閲覧をさせる
"""

import os
import glob
import re
import platform

from flask import (
	Flask,
	send_file,
	Response,
	abort,
	render_template,
	url_for,
)

import markdown
from waitress import serve

from template import Template
from converter import Converter

def main():
	Template.add_dir("templates/mytemplate")
	Template.add_dir("static/css")

	app = Flask(__name__)
	app_routing(app)
	
	os_name = platform.system()
	if os_name == "Windows":os.system('cls')
	else                   :os.system('clear')
	print("mymd")
	print("http://localhost:5000")
	#serve(app,port=5000)
	app.run(debug=True)

def app_routing(app):
	app.add_url_rule("/",view_func=index)
	app.add_url_rule("/<path:path>",view_func=output)

def index():
	print(Template.names())

	tab1 = Converter["tab"]()

	head = (
	f"""<link rel="stylesheet" href="{url_for('static', filename='css/index2.css')}">"""
	)
	
	return Template["html"](
		head = tab1(head),
		body = tab1(dir_linklist("mdfile")),
	)


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
	md_template = md.convert(a)

	css = f"""<link rel="stylesheet" href="{url_for('static', filename='css/mdfile.css')}">"""

	tab = Converter["tab"]()

	return Template["html"](
		title = None,
		head  = tab(css),
		body  = fold(md_template),
	)








def ttxt(txt):
	from textwrap import dedent
	return dedent(txt).strip()+"\n"

def dir_linklist(basepath,followdir=""):

	li     = Template["li"]
	link   = Template["link"]
	ul     = Template["ul"]
	fold   = Template["fold"]
	tab1   = Converter["tab"]()

	a = ""

	#ﾃﾞｨﾚｸﾄﾘに直接含まれるものを取得
	for path in sorted(glob.glob(f"{followdir}*.md",root_dir=basepath)):
		#followdir/aaa.md → aaa
		name     = os.path.splitext(os.path.basename(path))[0]

		#followdir/aaa.md → followdir/aaa
		linkpath = os.path.splitext(path)[0]	

		a+=li(link(
			link    = linkpath,
			display = name,
		))+"\n"

	#ﾃﾞｨﾚｸﾄﾘを取得
	for path in sorted(glob.glob(f"{followdir}*/",root_dir=basepath)): 
		foldcontent = fold(
			name = os.path.basename(os.path.normpath(path)),
			content = tab1(dir_linklist(basepath,followdir=path)),
		)

		a+= f"<li>{foldcontent}</li>\n"

	return ul(content=tab1(a.strip()))


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

























if __name__=="__main__":
	main()


