from pathlib import Path
from textwrap import dedent

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FileResource

from settings import settings
from src.resources.resources_info import general_directives

acl_examples_path = Path(settings.acl_examples).resolve()


def register_acl_example_resources(mcp: FastMCP) -> None:
    """Registra cada .aclscript da pasta de exemplos como um resource individual (uri fixa, sem parâmetro).

    Clientes sem suporte a resource templates (ex: Claude Desktop) só conseguem listar/ler
    resources concretos, então cada arquivo precisa de uma entrada própria além do template
    mcpr_get_acl_script_example. Times contribuem só jogando o .aclscript na pasta.
    """
    for file_path in sorted(acl_examples_path.glob("*.aclscript")):
        mcp.add_resource(
            FileResource(
                uri = f"arquivos://assets/acl_examples/{file_path.stem}",
                path = file_path,
                name = file_path.stem,
                description = dedent(f"""
                    {general_directives}

                    ## Description
                    Conteúdo do script de exemplo ACL "{file_path.stem}".
                """).strip(),
                mime_type = "text/plain",
            )
        )
