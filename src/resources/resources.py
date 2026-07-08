from typing import Annotated, Literal, Dict, Optional, List
from src.scraper.scraper import Scraper
import json
from src.LLM_Context.directives import directives
from settings import settings
import anyio
import re


acl_examples_path = anyio.Path(settings.acl_examples)

async def mcpr_list_acl_script_examples() -> dict:
    if not await acl_examples_path.exists():
        raise ValueError("A pasta com os exemplos do ACL, não foi encontrada ou não existe...")

    files = [
        p.stem
        async for p
        in acl_examples_path.iterdir()
        if re.match(r'.*\.aclscript$', p.name)
    ]

    if bool(files):
        return {"data": files}
    else:
        raise ValueError("A pasta com os exemplos do ACL está vazia")
    
async def mcpr_get_acl_script_example(
        nome_arquivo: Annotated[str, "O arquivo que será trazido do servidor para a LLM"]
) -> str:
    
    file_path = acl_examples_path / f"{nome_arquivo}.aclscript"
    if not await file_path.exists():
        raise ValueError("O arquivo não procurado não existe")
    
    content = await file_path.read_text(encoding='utf-8')
    return content

if __name__ == "__main__":
    import asyncio

    test1 = asyncio.run(mcpr_list_acl_script_examples())
    print(test1)
    
    test2 = asyncio.run(mcpr_get_acl_script_example(test1['data'][0]))
    print(test2)