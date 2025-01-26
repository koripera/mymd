import os
import string
import re

#task
#数字のﾌﾟﾚｰｽﾎﾙﾀﾞの対応
#ﾌｧｲﾙから取得するときの命名のﾙｰﾙ整備
#ﾌﾟﾚｰｽﾎﾙﾀﾞに使用する文字のｴｽｹｰﾌﾟ対応
#動的templateの作成

class meta_template(type):
	#ｸﾗｽに対して[]でｱｸｾｽできるようにする
	def __getitem__(cls,key):
		if key in cls.templates:
			return cls.templates[key]
		else:
			raise KeyError(f"{key} not found in {cls.__name__}")

class Template(metaclass = meta_template):
	templates = {}

	def __init__(self,template,blankets=None ):
		#文字列と、placeholderの囲いの形を指定する
		self.template = template
		self.blankets = blankets if blankets !=None else ("{","}")
		self.placenames = set()

		#placeholderの名前を取得しておく
		front,rear = self.blankets
		pattern = re.compile(f"{front}(?P<name>.*?){rear}")

		for match in re.finditer(pattern,self.template):
			self.placenames.add( match.group("name") )

	def __call__(self,*args,**kwargs):
		#対象がないものはｴﾗｰ	
		not_register = set(kwargs.keys()) - self.placenames
		if not_register:
			raise KeyError(f"not register:{not_register}")

			
		res = self.template
		front,rear = self.blankets

		#引数が収まらないときはｴﾗｰ
		if len(re.findall(f"{front}{rear}",res)) < len(args):
			raise TypeError("Too many arguments")
	
		#名前無しを置き換え
		for val in args:
			pattern = re.compile(f"{front}{rear}")
			res = re.sub(pattern,val,res,1)

		#余りを空白に
		pattern = re.compile(f"{front}{rear}")
		res = re.sub(pattern,"",res) 

		#名前付きプレースホルダを置き換えていく
		for name,val  in kwargs.items():
			val = val if val != None else ""
			pattern = re.compile(f"{front}{name}{rear}")
			res = re.sub(pattern,val,res)
	

		#未使用ﾌﾟﾚｰｽﾎﾙﾀﾞを空白にする
		for name in self.placenames-set(kwargs.keys()):
			pattern = re.compile(f"{front}{name}{rear}")
			res = re.sub(pattern,"",res)
		
			 

		return res

	@classmethod
	def add(cls, name, template ,blankets=None):
		cls.templates[name] = cls(template,blankets=blankets)

	@classmethod
	def add_file(cls, filepath,blankets=None):
		#fileからの追加
		name = os.path.splitext(os.path.basename(filepath))[0]
		with open(filepath,"r",encoding="utf-8") as f:
				template = f.read()

		#ﾌｧｲﾙ末尾の改行は削除
		if template[-1]=="\n":
			template = template[:-1]

		cls.add(
			name     = name,
			template = template,
			blankets = blankets,
		)

	@classmethod
	def add_dir(cls, directory,blankets=None):
		from glob import iglob
		for path in iglob(f"{directory}/*"):
			cls.add_file(path,blankets=blankets)

	@classmethod
	def names(cls):
		return list(cls.templates.keys())

class Dynamic_Template:
	#呼び出しの度に新しく内容を取得する
	def __init__(self):
		pass
