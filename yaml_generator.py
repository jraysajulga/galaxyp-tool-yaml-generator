import urllib2
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

response = urllib2.urlopen("https://galaxyp.msi.umn.edu/api/tools?in_panel=true",
                context=ctx)

data = json.loads(response.read())

for n in range(1,3):
    print data[n]['name']
    print len(data[n]['elems'])
    for tool in data[n]['elems']:
        if 'tool_shed_repository' in tool:
            print '  - name: ' + tool['tool_shed_repository']['name']
            print '\towner: ' + tool['tool_shed_repository']['owner']
            print '\ttool_panel_section_label: ' + tool['panel_section_name']
            
       
