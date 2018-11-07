import urllib2
import ssl
import json

def create_yaml_and_tabular(filename, url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib2.urlopen(url,
                    context=ctx)

    data = json.loads(response.read())

    yaml_file = open(filename + ".yaml", "w")

    yaml_file.write("---\n"
               "install_repository_dependencies: true\n"
               "install_resolver_dependencies: true\n"
               "install_tool_dependencies: false\n\n"
               "tools:\n")

    sheet_file = open(filename + ".tsv", "w")

    # Extracts section, name, and owner into output table
    output = list()
    for category in data:
        if 'elems' in category:
            for tool in category['elems']:
                if 'tool_shed_repository' in tool:
                    name = tool['tool_shed_repository']['name']
                    owner = tool['tool_shed_repository']['owner']
                    section = tool['panel_section_name']

                    output.append([section, name, owner])

    # Removes exact duplicates from the output list
    unique_list = list()
    for interlist in output:
        if interlist not in unique_list:
            unique_list.append(interlist)

    # Exports the data into a spreadsheet and galaxy YAML file
    for tool in unique_list:
        sheet_file.write("\t".join(tool) + "\n")
        yaml_file.write("\n".join(["  - name: " + tool[1],
                                    "\t\towner: " + tool[2],
                                    "\t\ttool_panel_section_label: " + tool[0],"\n"]))

    yaml_file.close()
    sheet_file.close()

#create_yaml_and_tabular("tools_galaxyp", "https://galaxyp.msi.umn.edu/api/tools?in_panel=true")
create_yaml_and_tabular("proteomicsEU_tools_galaxyp", "https://proteomics.usegalaxy.eu/api/tools?in_panel=true")
