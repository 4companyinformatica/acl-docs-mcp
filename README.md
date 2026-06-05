# ACL Analytics Helper — MCP Server

Servidor MCP que expõe a documentação oficial do **ACL Analytics (Diligent)** diretamente para LLMs, permitindo geração e revisão de scripts com sintaxe e lógica corretas.

---

## Como funciona

O servidor faz scraping da documentação oficial do ACL Analytics em tempo real (com cache local em disco) e disponibiliza três ferramentas para a LLM:

| Ferramenta                                     | Descrição                                                                                         |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `Get_ACL_Commands_or_Functions_List`         | Lista comandos ou funções da documentação, com filtros opcionais por nome e descrição         |
| `Get_ACL_Command_or_Function_Details`        | Retorna os detalhes completos de um comando ou função a partir do seu `href`                    |
| `Get_ACL_Scripting_Basic_Knowledge_and_Tips` | Retorna o contexto técnico sobre o ACL Analytics: objetos, estruturas, limitações e restrições |

O servidor também injeta um conjunto de **diretivas técnicas** (`instructions`) no contexto do cliente MCP, orientando a LLM a se comportar como especialista em ACL Analytics.

---

## Estrutura do Projeto

```
ACL-DOCS-MCP/
├── cache/                      # Cache local dos resultados do scraper (gerado em runtime)
├── src/
│   ├── LLM_Context/
│   │   ├── directives.py       # Diretivas técnicas injetadas no MCP (instructions)
│   │   └── tools_descriptions.py  # Descrições das ferramentas expostas ao cliente MCP
│   ├── scraper/
│   │   └── scraper.py          # Scraper da documentação do ACL Analytics
│   ├── server/
│   │   └── mcp.py              # Definição e configuração do servidor MCP (FastMCP)
│   ├── tools/
│   │   ├── tools_names.py      # Mapeamento de nomes internos → nomes MCP das ferramentas
│   │   └── tools.py            # Implementação das ferramentas MCP
│   └── util/
│       ├── cacher.py           # Cache em disco com TTL configurável
│       └── __init__.py
├── main.py                     # Entrypoint — executa o servidor via stdio
├── requirements.txt
└── .gitignore
```

---

## Instalação

**Pré-requisitos:** Python 3.10+

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ACL-DOCS-MCP.git
cd ACL-DOCS-MCP

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

---

## Execução

O servidor utiliza transporte  **stdio** , padrão do protocolo MCP:

```bash
python main.py
```

---

## Configuração no Claude Desktop

Adicione ao arquivo de configuração do Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "acl-analytics-helper": {
      "command": "python",
      "args": ["/caminho/absoluto/para/ACL-DOCS-MCP/main.py"]
    }
  }
}
```

> **Dica:** use o caminho absoluto do Python do seu `.venv` para garantir que as dependências sejam encontradas:
>
> ```json
> "command": "/caminho/para/ACL-DOCS-MCP/.venv/bin/python"
> ```

---

## Cache

O scraper salva os resultados em `cache/` com TTL de **24 horas** para evitar requisições desnecessárias à documentação. Os arquivos de cache são ignorados pelo `.gitignore`.

Para forçar atualização, basta apagar os arquivos dentro da pasta `cache/`.

---

## Dependências

| Pacote        | Versão mínima | Uso                                               |
| ------------- | --------------- | ------------------------------------------------- |
| `mcp`       | 1.27.1          | SDK do servidor MCP                               |
| `httpx`     | 0.28.1          | Requisições HTTP assíncronas                   |
| `bs4`       | 0.0.2           | Parsing do HTML da documentação                 |
| `starlette` | 1.1.0           | Framework ASGI (suporte futuro a transporte HTTP) |
| `uvicorn`   | 0.48.0          | Servidor ASGI                                     |

---

## Versão do ACL Analytics

Por padrão, o servidor aponta para a documentação da versão **19** do ACL Analytics. Para alterar, modifique o parâmetro `analytics_version` na instanciação do `Scraper` em `src/tools/tools.py`:

```python
scraper = Scraper(analytics_version="19")
```
