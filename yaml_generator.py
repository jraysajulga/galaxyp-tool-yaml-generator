import urllib2
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

response = urllib2.urlopen("https://galaxyp.msi.umn.edu/api/tools?in_panel=true",
                context=ctx)

data = json.loads(response.read())

file = open("tools_galaxyp.yaml", "w")

file.write("---\n"
           "install_repository_dependencies: true\n"
           "install_resolver_dependencies: true\n"
           "install_tool_dependencies: false\n\n"
           "tools:\n")

for category in data:
    if 'elems' in category:
        for tool in category['elems']:
            if 'tool_shed_repository' in tool:
                file.write("\n".join(["  - name: " + tool['tool_shed_repository']['name'],
                           "\t\towner: " + tool['tool_shed_repository']['owner'],
                           "\t\ttool_panel_section_label: " + tool['panel_section_name'],"\n"]))
            
       
file.close()
