"""
mdファイルをhtmlファイルに変換して、flaskでの閲覧をさせる
"""

import os
import glob
import re
import platform

from flask import Flask, send_file, Response, abort,render_template
import markdown
from waitress import serve



def main():
	Template.dir_register("static/css")
	temp_register()

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
	css = f"<style>\n{Template('index').nomal()}</style>\n"
	return css + dir_linklist("mdfile")

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

	css = f"<style>\n{Template('mdfile').nomal()}</style>\n"

	return css + fold(md_template)













def ttxt(txt):
	from textwrap import dedent
	return dedent(txt).strip()+"\n"

def dir_linklist(basepath,followdir=""):

	lilink = Template("lilink")
	ul     = Template("ul")
	fold   = Template("fold")

	a = ""

	#ﾃﾞｨﾚｸﾄﾘに直接含まれるものを取得
	for path in glob.iglob(f"{followdir}*.md",root_dir=basepath):
		#followdir/aaa.md → aaa
		name     = os.path.splitext(os.path.basename(path))[0]

		#followdir/aaa.md → followdir/aaa
		linkpath = os.path.splitext(path)[0]	

		a+=lilink(
			link    = linkpath,
			display = name,
		)

	#ﾃﾞｨﾚｸﾄﾘを取得
	for path in glob.iglob(f"{followdir}*/",root_dir=basepath): 
		foldcontent = fold(
			name = os.path.basename(os.path.normpath(path)),
			content = dir_linklist(basepath,followdir=path),
		)

		a+= f"<li>{foldcontent}</li>"

	return ul(content=a.strip())



class Template:
	templates = {}

	def __init__(self,name):
		if name in Template.templates:
			self.name = name
		else:
			raise ValueError(f"Template '{name}' does not exist")

	def __call__(self,**kwargs):
		try:
			return Template.templates[self.name].format(**kwargs)
		except KeyError as e:
			print(e)
			raise ValueError(f"Missing placeholder: {e.args[0]}") from None

	def nomal(self):
		return Template.templates[self.name]

	@classmethod
	def register(cls, name, template):
		cls.templates[name] = template

	@classmethod
	def dir_register(cls, directory):
		from glob import iglob
		for path in iglob(f"{directory}/*"):
			name = os.path.splitext(os.path.basename(path))[0]
			with open(path,"r",encoding="utf-8") as f:
				template = f.read()

			cls.register(
				name     = name,
				template = template
			)

	@classmethod
	def names(cls):
		return list(cls.templates.keys())
		
def temp_register():

	Template.register("link",ttxt(
	"""
	<a href='{link}' target='_blank'>{display}</a>
	"""
	))

	Template.register("lilink",ttxt(
	"""
	<li><a href='{link}' target='_blank'>{display}</a></li>
	"""
	))

	Template.register("ul",ttxt(
	"""
	<ul>
	{content}
	</ul>
	"""
	))

	Template.register("fold",ttxt(
	"""
	<details open>
	<summary>{name}</summary>
	{content}
	</details>
	"""
	))





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


