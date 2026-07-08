
from mcp.server.fastmcp import FastMCP
from src.tools.tools import *
from src.resources.resources import *
from src.tools.tools_names import tools_names
from src.LLM_Context.directives import directives
from src.tools.tools_descriptions import tools_descriptions
from src.resources.resources_info import resources_info
from src.resources.dynamic_resources import register_acl_example_resources
from settings import settings


mcp = FastMCP(name=settings.mcp_server_name, instructions=directives)

tools = {tool_name: tool_func for tool_name, tool_func in globals().items() if tool_name.startswith("mcp_") and callable(tool_func)}
resources = {resource_name: resource_func for resource_name, resource_func in globals().items() if resource_name.startswith("mcpr_") and callable(resource_func)}

for tool_name, tool_func in tools.items():
    mcp.add_tool(
        fn=tool_func,
        name=tools_names.get(tool_name, tool_name.replace("mcp_", "")),
        description=tools_descriptions.get(tool_name)
    )

for resource_name, resource_func in resources.items():
    info = resources_info[resource_name]
    mcp.resource(
        info["uri"],
        name=info.get("name", resource_name.replace("mcpr_", "")),
        description=info["description"],
        mime_type=info.get("mime_type"),
        icons = info.get("icons"),
        annotations=info.get("annotations"),
        meta=info.get("meta")
    )(resource_func)

register_acl_example_resources(mcp)

if settings.streamable_http_path:
    mcp.settings.streamable_http_path = settings.streamable_http_path

if __name__ == "__main__":
    print(
        mcp.settings
    )