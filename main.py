from argparse import ArgumentParser
from src.server.mcp import mcp
import uvicorn
from starlette.applications import Starlette
from src.server.routes import Routes
from src.middlewares.auth import ASGIAuth
from settings import settings
import contextlib


parser = ArgumentParser(description="Launches the MCP Server")
parser.add_argument("-t", "--transport", type=str, default="stdio", help="Transport method for MCP (e.g., stdio, http)", choices=["stdio", "http"])
parser.add_argument("-hn", "--hostname", type=str, default="127.0.0.1", help="Hostname for the MCP server")
args = parser.parse_args()

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
     async with contextlib.AsyncExitStack() as stack:
          # TODO: Adicionar boas vindas
          # TODO: Estudar outros contextos possíveis, como conexões com outros serviços, etc.
          await stack.enter_async_context(mcp.session_manager.run())
          yield
          # TODO: Adicionar despedida

if args.transport == "http":
    app = Starlette(lifespan=lifespan, routes=Routes)
    app.add_middleware(ASGIAuth)

if __name__ == "__main__":

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "http":    
        uvicorn.run("main:app", host=args.hostname, port=settings.server_port, reload=True)
