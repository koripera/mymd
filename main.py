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

indexcss=("""\
<style>
details > summary {
  list-style: none;
}
ul {
    list-style-type: none;
}
ul {
  box-shadow :0px 0px 3px silver;
  border: solid 1px whitesmoke;
  padding: 0.5em 1em 0.5em 2.3em;
  position: relative;
  background: #fafafa;
}

ul li {
  line-height: 1.5;
  padding: 0.5em 0;
  list-style-type: none!important;
}

ul li:before {
  font-family: "Font Awesome 5 Free";
  content: "\f0da";
  position: absolute;
  left : 1em; /*左端からのアイコンまで*/
  color: gray; /*アイコン色*/
}
</style>
""")


app = Flask(__name__)


@app.route("/")
def index(): 
	return indexcss+dir_linklist("mdfile")



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

	@classmethod
	def register(cls, name, template):
		cls.templates[name] = template

	@classmethod
	def list_templates(cls):
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
	temp_register()
	os_name = platform.system()
	if os_name == "Windows":os.system('cls')
	else                   :os.system('clear')
	print("mymd")
	print("http://localhost:5000")
	#serve(app,port=5000)
	app.run(debug=True)


