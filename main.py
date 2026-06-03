from argparse import ArgumentParser
from src.server.mcp import mcp
import uvicorn
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse


if __name__ == "__main__":

    parser = ArgumentParser(description="Launches the MCP Server")
    parser.add_argument("-t", "--transport", type=str, default="stdio", help="Transport method for MCP (e.g., stdio, http)", choices=["stdio", "http"])
    parser.add_argument("-hn", "--hostname", type=str, default="127.0.0.1", help="Hostname for the MCP server")
    args = parser.parse_args()

    params = {"transport": args.transport}

    if args.transport == "http":
        params = {
            "host": "0.0.0.0",
            "port": 8000
        }
        
    mcp.run(**params)