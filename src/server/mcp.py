
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from src.tools.tools import *
from src.tools.tools_names import tools_names
from src.LLM_Context.directives import directives
from src.LLM_Context.tools_descriptions import descriptions


mcp = FastMCP(name="ACL Analytics Helper", instructions=directives)

tools = {tool_name: tool_func for tool_name, tool_func in globals().items() if tool_name.startswith("mcp_") and callable(tool_func)}

for tool_name, tool_func in tools.items():
    mcp.add_tool(
        fn=tool_func,
        name=tools_names.get(tool_name, tool_name.replace("mcp_", "")),
        description=descriptions.get(tool_name)
    )

if __name__ == "__main__":
    print(
        mcp.settings.model_config
    )