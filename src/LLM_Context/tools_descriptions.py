from src.tools.tools_names import tools_names

general_directives = f"""## Diretivas Gerais:
Use the tools from this server EVERYTIME a user asks about ACL Analytics commands, functions, header tags, or how to do something in ACL Analytics.
Check the {tools_names.get("mcp_get_acl_scripting_tips", "Get_ACL_Scripting_Basic_Knowledge_and_Tips")} at least once to understand how ACL Analytics works, its objects and structures, and its limitations. This will help you to make better queries to the {tools_names.get("mcp_get_acl_commands_or_functions_list", "Get_ACL_Commands_or_Functions_List")}, {tools_names.get("mcp_get_acl_command_or_function_details", "Get_ACL_Command_or_Function_Details")}, {tools_names.get("mcp_get_acl_header_tags_list", "Get_ACL_Header_Tags_List")} and {tools_names.get("mcp_get_acl_header_tag_details", "Get_ACL_Header_Tag_Details")}).
"""

descriptions = {
    "mcp_get_acl_commands_or_functions_list": f"""
{general_directives}

## Description
Fetches the list of commands or functions from the ACL Analytics documentation. 
You can specify whether to fetch commands or functions, and optionally filter the results by command name or description.

## Here are some examples of users' queries that this tool can answer:
* "List all commands in ACL Analytics."
* "How do I use JOIN in Analytics?" (filtering by command name)
* "How can I retrieve data ODBC in ACL?" (filtering by description)
""",
# ==================================================
    "mcp_get_acl_command_or_function_details": f"""
{general_directives}

## Description
Fetches the details of a command or function from the ACL Analytics documentation. 
You need to provide the href of the command or function and specify whether it is a command or a function.
You can retrieve the href from the mcp_get_acl_commands_or_functions_list tool

## Here are some examples of users' queries that this tool can answer:
* "How can I remove duplicates from a table?" (after finding the command SUMMARIZE href, return the explanation using this tool)
* "Give me an example of how to use "RECOFFSET()" in ACL Analytics" (after finding the function RECOFFSET() href, return the explanation and example using this tool)
""",
# ==================================================
    "mcp_get_acl_scripting_tips": f"""
{general_directives}

## Description
Fetches information about ACL Analytics, including: how it works, objects and structures available, limitations and restrictions

## Examples:
* "Are there arrays in ACL Analytics?"
* "Can ACL return system variables from Windows environment variables?"
""",
# ==================================================
    "mcp_get_acl_header_tags_list": f"""
{general_directives}

## Description
Fetches the list of analytic header tags from the ACL Analytics documentation.
Header tags are special directives placed at the top of ACL scripts to define metadata such as script type, version, input parameters, and passwords.
Each tag has a type (e.g. ANALYTIC, PARAM, PASSWORD), a name, a description, and an href to its detail page.
You can optionally filter results by tag name, tag type, or description.

## Examples:
* "What tags can I use in an ACL script header?"
* "How do I declare a parameter in an ACL script?" (filter by tag_type='PARAM' or tag_name)
* "What is the //PASSWORD tag?" (filter by tag_name)
""",
# ==================================================
    "mcp_get_acl_header_tag_details": f"""
{general_directives}

## Description
Fetches the full documentation page for a specific ACL analytic header tag.
You need the href of the tag, which you can retrieve from {tools_names.get("mcp_get_acl_header_tags_list", "Get_ACL_Header_Tags_List")}.

## Examples:
* "Show me the full syntax of the //PARAM tag."
* "Give me a complete example of the //ANALYTIC tag."
"""
}