from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from src.server.mcp import mcp
from settings import settings
import contextlib


def info(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "status": "MCP Server is running",
                "version": settings.server_version
            }
        )

Routes = [
    Route("/info", info, methods=["GET"]),
    Mount("/", mcp.streamable_http_app())
]
    
    
if __name__ == "__main__":
    pass