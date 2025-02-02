
#文字列を加工して、文字列を返す関数を扱う
#変更内容を可変にするために関数を返す関数を中継して使う

#convert_func  = Converter["name"](args)
#newtxt = convert_func(txt)

class meta(type):
	#ｸﾗｽに対して[]でｱｸｾｽできるようにする
	def __getitem__(cls,key):
		if key in cls.items:
			return cls.items[key]
		else:
			raise KeyError(f"{key} not found in {cls.__name__}")

class Converter(metaclass = meta):
	#関数を返す関数を登録
	items = {}

	@classmethod	
	def add(cls,func):
		#print("aaa")
		cls.items[func.__name__]=func

@Converter.add
def tab(level=1):
	def func(txt):
		lines = txt.split("\n")
		return "\n".join(["\t"*level+line for line in lines])
		
	return func


