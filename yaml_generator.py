import urllib2
import ssl
import json
import re

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

def matrix_to_dict(matrix):
    output = {"section" : [],
              "name" : [],
              "owner" : []}
    for row in matrix:
        output["section"].append(row[0])
        output["name"].append(row[1])
        output["owner"].append(row[2])

    return output


def remove_duplicates(duplicate_list):
    # Removes exact duplicates
    unique_list = []
    for interlist in duplicate_list:
        if interlist not in unique_list:
            unique_list.append(interlist)

    tool_dict = matrix_to_dict(unique_list)
    output = []
    final_indices = []
    finished_tools = []
    for interlist in unique_list:
        if interlist[1] not in finished_tools:
            indices = [i for i, x in enumerate(tool_dict["name"]) if x == interlist[1]]
            finished_tools.append(interlist[1])
            if len(indices) > 1:
                owners = [tool_dict["owner"][i] for i in indices]
                sections = [tool_dict["section"][i] for i in indices]
                print "SDF"
                print owners
                print sections
                for i in indices:    
                    print indices
                    print tool_dict["name"][i]
                    print tool_dict["owner"][i]
                    print tool_dict["section"][i]
                    
                print '____'
            else:
                output.append([tool_dict["section"][indices[0]],
                               tool_dict["name"][indices[0]],
                               tool_dict["owner"][indices[0]]])
                                                         
    return output

# Checks name and owner of added tools for any rows already
# defined in the original tool list
def remove_unnecessary_tools(original_tools, added_tools):
    output = []
    for add_tool in added_tools:
        necessary = True
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


def exportTools():
    proteomicsEU_tools = json_to_tabular("proteomicsEU", "https://proteomics.usegalaxy.eu/api/tools?in_panel=true")
    galaxyp_tools = json_to_tabular("galaxyp","https://galaxyp.msi.umn.edu/api/tools?in_panel=true")
    galaxyp_tools = remove_unnecessary_tools(proteomicsEU_tools, galaxyp_tools)

    export_yaml_and_sheet(remove_duplicates(galaxyp_tools))

def removeCommonTools(ref_filename, trim_filename):
    
    ref_yaml = open(ref_filename)
    line = ref_yaml.readline()
    while not re.search('tools:', line):
        line = ref_yaml.readline()

    ref_tools = {}
    for line in ref_yaml:
        m = re.search('- name: ([\w,\- ]+)', line)
        if m:
            name = m.group(1)
            line = ref_yaml.next()
            owner = re.search('\s+owner: ([\w,\- ]+)', line).group(1)
            line= ref_yaml.next()
            if name in ref_tools:
                if owner != ref_tools[name]:
                    if isinstance(ref_tools[name], list):
                        ref_tools[name].append(owner)
                    else:
                        ref_tools[name] = [ref_tools[name], owner]
            else:
                ref_tools[name] = owner

    output_filename = "website/trimmed_tools_galaxyp.yaml"
    open(output_filename, 'w').close()
    output = open(output_filename, "a")
    trim_yaml = open(trim_filename)
    line = trim_yaml.readline()
    while not re.search('tools:', line):
        line = trim_yaml.readline()
        output.write(line)
    for line in trim_yaml:
        m = re.search('- name: ([\w,\- ]+)', line)
        if m:
            name = m.group(1)
            line = trim_yaml.next()
            owner = re.search('\s+owner: ([\w,\- ]+)', line).group(1)
            line= trim_yaml.next()
            section = re.search('\s+tool_panel_section_label: ([\w,\- ]+)', line).group(1)

            if name in ref_tools.keys():
                if owner != ref_tools[name]:
                    output.write("\n".join(["  - name: " + name,
                                    "\t\towner: " + owner,
                                    "\t\ttool_panel_section_label: " + section,"\n"]))
            else:
                output.write("\n".join(["  - name: " + name,
                                    "\t\towner: " + owner,
                                    "\t\ttool_panel_section_label: " + section,"\n"]))
            

    
    output.close()
    trim_yaml.close()
    ref_yaml.close()
    


removeCommonTools('website/tools_iuc.yaml', 'website/tools_galaxyp.yaml')
    

