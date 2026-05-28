import argparse
from src.server.mcp import mcp
import uvicorn
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse


if __name__ == "__main__":
    mcp.run(transport='stdio')