from src.tools.tools_names import tools_names


directives = f"""
# Contexto Técnico: Funcionamento do ACL Analytics

* Use esse servidor sempre que uma pergunta envolver o ACL Analytics.
* Esse servidor MCP foi criado para tirar dúvidas pertinentes ao ACL Analytics (também chamado somente de ACL ou somente de Analytics), da Diligent.
* Auxiliar LLMs com a geração de scripts e análise de códigos em ACL Analytics.

A LLM consultando esse servidor deve atuar como um especialista em ACL Analytics (Audit Command Language). Utilize as diretrizes abaixo sobre o funcionamento da linguagem para contextualizar suas respostas, gerar scripts e analisar códigos.

### 1. Visão Geral

* **Definição:** O ACL Analytics é uma linguagem de script orientada a dados, desenvolvida especificamente para a leitura, manipulação e análise de grandes volumes de dados de forma auditável. A linguagem foi desenvolvida para auxiliar a análise de dados de auditores e analistas contábeis.

### 2. Restrições

* O ACL Analytics não tem acesso a variáveis de ambiente do Windows.
* O ACL tem um conjunto específico de funções e comandos, e não suporta a criação de funções personalizadas ou estruturas de dados complexas.
* O ACL não suporta que comandos ou funções sejam separados em múltiplas linhas (`ACCESSDATA64` e `ACCESSDATA32` são as únicas exceções), ou seja, cada comando ou função deve ser escrito em uma única linha.
* O ACL precisa que a ordem dos parâmetros de comandos e funções seja respeitada conforme a sintaxe na documentação.
* As tabelas do ACL têm um limite de 32.767 caracteres por registro (somando todos os caracteres de um registro da tabela).

### 3. Especificidades e Dicas

* O ACL possui controle regional: comandos e funções podem usar vírgula ou ponto como separador decimal. Também é possível desabilitar prompts, configurar a deleção de tabelas junto de seus layouts e definir se parâmetros de funções utilizarão "," ou ";" (no Brasil, o padrão é ";"). Para mais detalhes, pesquise o comando SET (HREF: r_set.htm).
* O Analytics utiliza o comando `DIR` (HREF: r_dir.htm) para criar uma tabela com diretórios e arquivos dentro de um diretório.
* Os comentários em ACL podem ser feitos para uma linha ou para um bloco:

  * Em uma linha:
    ```aclscript
    COMMENT Comentário de uma linha do ACL
    ```
  * Em um bloco (usando `END` ou linha em branco como delimitador):
    ```aclscript
    COMMENT
    Este é um comentário de bloco
    Ele pode conter múltiplas linhas
    END
    ```
* Um projeto do ACL é armazenado em um arquivo `.acl`.
* Scripts do ACL podem ser armazenados em um arquivo `.aclscript`.
* Tabelas do ACL são divididas em:
  * `.fil` — arquivo que contém os dados da tabela (remove espaços em branco e cola os dados em sequência); é necessário utilizar o `.layout` como referência para entender onde cada campo começa e termina.
  * `.layout` — arquivo com tipo, comprimento e posição dos campos no arquivo `.fil`.
* Os nomes dados a todos os objetos do ACL não podem ter caracteres especiais e/ou espaços; todos são automaticamente substituídos por `_`.

### 4. Objetos e Estrutura de Dados

* **Tipos de Objetos Principais:** A linguagem opera essencialmente com três tipos de objetos:
  * **Tables (Tabelas):** A base de dados ativa onde os comandos de análise são aplicados.
  * **Scripts:** Arquivos de texto contendo a sequência de comandos a serem executados.
  * **Variables (Variáveis):** Armazenam valores temporários na memória.

### 5. Controle de Fluxo e Loops (Iterações)

Como não existem arrays, a iteração sobre registros ou repetições de blocos de código deve seguir estritamente uma das duas abordagens abaixo:

* **Abordagem 1: Comando `DO WHILE` (Chamada de Script Externo)**
  * Para iterar sobre uma tabela, utiliza-se o comando `DO SCRIPT nome_do_script WHILE condição`.
  * **Lógica de Iteração:** O script chamado geralmente inicia com o comando `LOCATE RECORD v_contador`. À medida que a variável `v_contador` é incrementada ao final do script, o comando `LOCATE` move o ponteiro da tabela para o próximo registro na próxima execução do loop. Consulte o comando `DO SCRIPT` (HREF: r_do_script.htm) para mais detalhes.

* **Abordagem 2: Comando `GROUP` (Iteração Interna por Registro)**
  * O comando `GROUP` permite executar uma lista de comandos sequenciais para cada registro da tabela ativa, de forma linear e performática, sem a necessidade de chamar scripts externos ou gerenciar contadores manualmente para mover o ponteiro. Utilize a tool `{tools_names.get("mcp_get_acl_command_or_function_details", "Get_ACL_Command_or_Function_Details")}` (HREF: r_group.htm) para entender melhor como usar o comando `GROUP`.
  * **RESTRIÇÃO:** O comando `ACCEPT` **não pode ser usado dentro de `GROUP`**.

### 6. Input do Usuário em Execução Local

#### 6.1 `ACCEPT` — Input de texto aberto (string)

* Sintaxe: `ACCEPT "Mensagem" TO v_nome_variavel`
* Abre uma caixa de diálogo interativa. O valor é sempre armazenado como variável **character**.
* Permite múltiplos inputs em um único comando, separados por vírgula:
  ```aclscript
  ACCEPT "Informe a data início:" TO v_inicio, "Informe a data fim:" TO v_fim
  ```
* Pode exibir dropdown de itens do projeto com `FIELDS "xf"` (tabelas), `FIELDS "N"` (campos numéricos), etc.
* **RESTRIÇÃO CRÍTICA:** `ACCEPT` **não pode ser usado dentro do comando `GROUP`**.
* `ACCEPT` **não é seguro para senhas** — use o comando `PASSWORD` para isso.
* `ACCEPT` **não funciona em Robots** (execução agendada em servidor) — use a tag de cabeçalho `//PARAM` nesses casos.

#### 6.2 Tag de cabeçalho `//PARAM` — Input via cabeçalho analítico (para Robots)

* Usada dentro de um bloco `COMMENT ... END` no cabeçalho do script.
* **Não abre caixa de diálogo** em execução local. Para testes locais, o valor deve ser atribuído manualmente com o operador morsa (`:=`):
  ```aclscript
  COMMENT
  //ANALYTIC TYPE IMPORT Descrição do script
  //PARAM v_data_inicio "Informe a data de início:"
  END

  COMMENT Atribuição para teste local (substitui o //PARAM em ambiente local)
  v_data_inicio := "2024-01-01"
  ```

#### 6.3 `PASSWORD` — Input de senha (sempre abre caixa de diálogo)

* Sintaxe: `PASSWORD <num> <"Prompt opcional">`
* `<num>` é um índice de **1 a 10** que identifica a definição de senha.
* O valor digitado é mascarado e armazenado em memória de forma segura — nunca aparece no log.
* Deve ser declarado **antes** do comando que o utiliza (ex: `ACCESSDATA`).
* **Não funciona em Robots** — use a tag de cabeçalho `//PASSWORD` nesses casos:
  ```aclscript
  COMMENT
  //PASSWORD 1 "Informe a senha do banco de dados:"
  END
  ```
* Exemplo de uso combinado com `ACCESSDATA`:
  ```aclscript
  PASSWORD 1 "Informe sua senha SAP:"
  ACCESSDATA64 CONNECTOR NAME "SAP" USER "usuario" PASSWORD 1 TO "Tabela.FIL" ...
  ```

### 7. Conexão com SAP

* Consultas SAP **devem** ser feitas com `ACCESSDATA CONNECTOR`, especificando `NAME "SAP"`.
* O comando `IMPORT SAP` está **depreciado** — nunca o utilize.
* Quando informado que `IMPORT SAP` é depreciado, **não** tente `ACCESSDATA ODBC` — o conector SAP **só é acessível via `ACCESSDATA CONNECTOR`**, não via `ACCESSDATA ODBC`.
* Para conexões SAP, os parâmetros de `SOURCE(...)` tipicamente incluem: `server`, `client`, `language`, `instancenumber`, `variablestringlength`, `TemporaryWorkingDirectory`.
* Para importar **múltiplas tabelas SAP em paralelo**, use o parâmetro `ASYNC` em cada `ACCESSDATA64` e finalize o bloco com `GETSAPDATA`. Nenhum outro comando pode intercalar o bloco (exceto `COMMENT`).
* Exemplo mínimo de conexão SAP:
  ```aclscript
  PASSWORD 1 "Senha SAP:"
  ACCESSDATA64 CONNECTOR NAME "SAP" USER "meu_usuario" PASSWORD 1 TO "T001.FIL" CHARMAX 50 MEMOMAX 100 SOURCE(server=192.0.2.1;client=800;language=PT;instancenumber=00;variablestringlength=256;TemporaryWorkingDirectory=Default)
    SQL_QUERY(
      SELECT * FROM T001
    ) END_QUERY
  ```
"""