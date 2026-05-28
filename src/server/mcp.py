
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from src.tools.tools import command_list_tool, command_details_tool
from src.LLM_Context.general import directives
from src.LLM_Context.tools_descriptions import descriptions


mcp = FastMCP(name="ACL Analytics Documentation MCP", instructions=directives)

tools = {tool_name: tool_func for tool_name, tool_func in globals().items() if tool_name.endswith("_tool") and callable(tool_func)}

for tool_name, tool_func in tools.items():
    mcp.add_tool(
        fn=tool_func,
        name=tool_name.replace("_tool", ""),
        description=descriptions.get(tool_name)
    )

if __name__ == "__main__":
    pass