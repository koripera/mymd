import os
import string

class DefaultDict(dict):
	def __missing__(self,key):
		return ""

def placeholder(template):
	#ﾌﾟﾚｰｽﾎﾙﾀﾞの名前を取得する
	formatter = string.Formatter()
	placeholders = [field_name for _,field_name,_,_ in formatter.parse(template) if field_name]
	return placeholders

class Template:
	templates = {}

	def __init__(self,name):
		if name in Template.templates:
			self.name = name
		else:
			raise NameError(f"Template '{name}' does not exist")

	def __call__(self,**kwargs):
		#ﾌﾟﾚｰｽﾎﾙﾀﾞのﾃﾞﾌｫﾙﾄは空文字列、対象外指定はｴﾗｰ
		places = placeholder(Template.templates[self.name])
		not_register=[name for name in kwargs.keys() if name not in places]		
		if not_register:
			raise NameError(f"The following is not included::{not_register}")
			
		return Template.templates[self.name].format_map(DefaultDict(kwargs))

	def raw(self):
		return Template.templates[self.name]

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
