import urllib2
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

response = urllib2.urlopen("https://galaxyp.msi.umn.edu/api/tools?in_panel=true",
                context=ctx)

data = json.loads(response.read())

yaml_file = open("tools_galaxyp.yaml", "w")

yaml_file.write("---\n"
           "install_repository_dependencies: true\n"
           "install_resolver_dependencies: true\n"
           "install_tool_dependencies: false\n\n"
           "tools:\n")

sheet_file = open("tools_galaxyp.tsv", "w")

cache = {"name" : [],
         "owner" : [],
         "section" : []}
for category in data:
    if 'elems' in category:
        for tool in category['elems']:
            if 'tool_shed_repository' in tool:
                name = tool['tool_shed_repository']['name']
                owner = tool['tool_shed_repository']['owner']
                section = tool['panel_section_name']

                if name in cache["name"]:
                    index = cache["name"].index(name)
                    if cache["owner"][index] != owner and cache["section"][index] != section:
                            yaml_file.write("\n".join(["  - name: " + name,
                                    "\t\towner: " + owner,
                                    "\t\ttool_panel_section_label: " + section,"\n"]))
                
                            sheet_file.write(section +
                                             '\t' + name +
                                             '\t' + owner + '\n')
                else:
                    yaml_file.write("\n".join(["  - name: " + name,
                                    "\t\towner: " + owner,
                                    "\t\ttool_panel_section_label: " + section,"\n"]))
                
                    sheet_file.write(section +
                                     '\t' + name +
                                    '\t' + owner + '\n')
yaml_file.close()
sheet_file.close()
