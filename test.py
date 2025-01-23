from template import Template

Template.add_dir("templates/mytemplate")

a = Template("html")

a = a(title="aaa")

print(a)
