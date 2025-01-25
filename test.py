from template2 import Template

Template.add_dir("templates/mytemplate")

#a = Template["html"]
#a = Template("aaa{}uuu{}")("00","01")
#b = Template("{aaa}{iii}")(aaa="aiueo")
#Template.add("aaa","{aaa}{iii}")

print(Template["html"](body="aiueo"))


