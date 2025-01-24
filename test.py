from template2 import Template

#Template.add_dir("templates/mytemplate")

#a = Template["html"]
a = Template("aaa{}uuu{}")("00","01","02")

b = "{}{}{}"
print(b.format("a","b","c"))

print(a)
