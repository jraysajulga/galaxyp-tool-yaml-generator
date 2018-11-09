import urllib2
import ssl
import json

def json_to_tabular(label, url):

    # Loads JSON from the provided URL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib2.urlopen(url,
                    context=ctx)
    data = json.loads(response.read())

    # Arranges section, name, and owner from JSON into tabular output
    output = list()
    for category in data:
        if 'elems' in category:
            for tool in category['elems']:
                if 'tool_shed_repository' in tool:
                    name = tool['tool_shed_repository']['name']
                    owner = tool['tool_shed_repository']['owner']
                    section = tool['panel_section_name']

                    output.append([section, name, owner])
                    
    return output


def remove_exact_duplicates(duplicate_list):
    # Removes exact duplicates from the output list
    unique_list = list()
    for interlist in duplicate_list:
        if interlist not in unique_list:
            unique_list.append(interlist)
    return unique_list

# Checks name and owner of added tools for any rows already
# defined in the original tool list
def remove_unnecessary_tools(original_tools, added_tools):
    necessary = True
    output = []
    for add_tool in added_tools:
        for orig_tool in original_tools:
            if add_tool[1] == orig_tool[1] and add_tool[2] == orig_tool[2]:
                    necessary = False
                    break
        if necessary:
            output.append(add_tool)
    return output
                    

def export_yaml_and_sheet(unique_list):
    filename = "tools_galaxyp"
    
    yaml_file = open(filename + ".yaml", "w")

    yaml_file.write("---\n"
               "install_repository_dependencies: true\n"
               "install_resolver_dependencies: true\n"
               "install_tool_dependencies: false\n\n"
               "tools:\n")

    sheet_file = open(filename + ".tsv", "w")

    # Exports the data into a spreadsheet and galaxy YAML file
    for tool in unique_list:
        sheet_file.write("\t".join(tool) + "\n")
        yaml_file.write("\n".join(["  - name: " + tool[1],
                                    "\t\towner: " + tool[2],
                                    "\t\ttool_panel_section_label: " + tool[0],"\n"]))

    yaml_file.close()
    sheet_file.close()


proteomicsEU_tools = json_to_tabular("proteomicsEU", "https://proteomics.usegalaxy.eu/api/tools?in_panel=true")
galaxyp_tools = json_to_tabular("galaxyp","https://galaxyp.msi.umn.edu/api/tools?in_panel=true")
galaxyp_tools = remove_unnecessary_tools(proteomicsEU_tools, galaxyp_tools)

export_yaml_and_sheet(remove_exact_duplicates(galaxyp_tools))
