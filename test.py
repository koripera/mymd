from template import Template
from converter import Converter

Template.add_dir("templates/mytemplate")

#a = Template["html"]
#a = Template("aaa{}uuu{}")("00","01")
#b = Template("{aaa}{iii}")(aaa="aiueo")
#Template.add("aaa","{aaa}{iii}")

#print(Template["html"](body="aiueo"))

#aaa = Converter["tab"](1)
#print(aaa("aiueo"))

aaa = Template["html"].prefill(
	head="",
	body="aaa",
)

print(aaa.placenames)

print(aaa("konnitiwa"))
