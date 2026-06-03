from src.tools.tools_names import tools_names

general_directives = f"""## Diretivas Gerais:
Use the tools from this server EVERYTIME a user asks about ACL Analytics commands, functions, or how to do something in ACL Analytics.
Check the {tools_names.get("mcp_get_acl_scripting_tips", "Get_ACL_Scripting_Basic_Knowledge_and_Tips")} at least once to understand how ACL Analytics works, its objects and structures, and its limitations. This will help you to make better queries to the {tools_names.get("mcp_get_acl_commands_or_functions_list", "Get_ACL_Commands_or_Functions_List")} and {tools_names.get("mcp_get_acl_command_or_function_details", "Get_ACL_Command_or_Function_Details")}).
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
"""
}