import os
import glob



def ttxt(txt):
	from textwrap import dedent
	return dedent(txt).strip()+"\n"

def dir_linklist(basepath):

	lilink = Template("lilink")
	ul = Template("ul")
	fold = Template("fold")

	htmltxt = ""

	#ﾃﾞｨﾚｸﾄﾘに直接含まれるものを取得
	a = ""
	
	for path in glob.iglob("*.md",root_dir=basepath):
		name = os.path.basename(path)
		linkpath = os.path.join(basepath,path)		

		a+=lilink(
			link    = linkpath,
			display = name,
		)

	#ﾃﾞｨﾚｸﾄﾘを取得
	for path in glob.iglob('*/',root_dir=basepath):
		a += fold(
			name = basepath,
			content = dir_linklist(os.path.join(basepath,path))
		)

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
	<details>
	\t<summary>{name}</summary>
	{content}
	</details>
	"""	))

#temp_register()
#res = dir_linklist("mdfile")

#print(res)
