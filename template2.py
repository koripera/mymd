import os
import string
import re

class DefaultDict(dict):
	def __missing__(self,key):
		return ""

def placeholder(template):
	#ﾌﾟﾚｰｽﾎﾙﾀﾞの名前を取得する
	formatter = string.Formatter()
	placeholders = [field_name for _,field_name,_,_ in formatter.parse(template) if field_name]
	return placeholders

class meta_template(type):
	#ｸﾗｽに対して[]でｱｸｾｽできるようにする
	def __getitem__(cls,key):
		if key in cls.templates:
			return cls.templates[key]
		else:
			raise KeyError(f"{key} not found in {cls.__name__}")

class Template(metaclass = meta_template):
	templates = {}

	def __init__(self,template,blankets=("{","}") ):
		#文字列と、placeholderの囲いの形を指定する
		self.template = template
		self.blankets = blankets
		self.placenames = set()

		#placeholderの名前を取得しておく
		front,rear = self.blankets
		pattern = re.compile(f"{front}(?<name>.*?){rear}")

		for match in re.finditer(pattern,self.template):
			self.placenames.add( match.groups("name") )

	def __call__(self,*args,**kwargs):
		#対象がないものはｴﾗｰ	
		not_register = set(kwargs.keys()) - self.placenames
		if not_register:
			raise KeyError(f"not register:{not_register}")
			
		res = self.template
		front,rear = self.blankets
		
		#名前無しを置き換え
		for val in args:
			pattern = re.compile(f"{front}{rear}")
			res = re.sub(pattern,val,res,1)

		#名前付きプレースホルダを置き換えていく
		for name,val  in kwargs.items():
			pattern = re.compile(f"{front}{name}{rear}")
			res = re.sub(pattern,val,res)

		return res

	@classmethod
	def add(cls, name, template):
		cls.templates[name] = template

	@classmethod
	def add_file(cls, filepath):
		#fileからの追加
		name = os.path.splitext(os.path.basename(filepath))[0]
		with open(filepath,"r",encoding="utf-8") as f:
				template = f.read()

		cls.add(
			name     = name,
			template = template
		)

	@classmethod
	def add_dir(cls, directory):
		from glob import iglob
		for path in iglob(f"{directory}/*"):
			cls.add_file(path)

	@classmethod
	def names(cls):
		return list(cls.templates.keys())

class Dynamic_Template:
	def __init__(self):
		pass
