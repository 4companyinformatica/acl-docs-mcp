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

    COMMENT
    Este é outro comentário de bloco
    Ele pode conter múltiplas linhas
    
    COMMENT Este bloco está separado do comentário acima
    OPEN Table1
    ```
* Os comentários em aclscript não podem ser colocados na mesma linha que um comando
```aclscript
COMMENT Isso causaria um erro:
DIR *.acl TO Table_Test COMMENT Test table for debug
```
* Comentários em ACL não podem utilizar o caractere `=`.
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
  * Exemplo:

  ```aclscript
  COMMENT Nome desse Script: S00_Cabecalho_Loop
  OPEN Table1
  COMMENT Nesse exemplo, o layout da tabela Table1 tem "user_name" e "user_email"

  COUNT
  COMMENT COUNT1 é gerado automaticamente quando se roda o comando COUNT, mostra a quantidade de registros da tabela ativa
  V_Limite = COUNT1
  V_Counter = 1
  V_List = ""

  DO S01_Loop WHILE V_Limite <= V_Counter
  ```

  ```aclscript
  COMMENT Nome desse Script: S01_Loop
  OPEN Table1
  LOCATE RECORD %V_Counter%

  V_CurName = ALLTRIM(user_name)
  IF (V_Counter = 1) ASSIGN V_List = V_CurName
  IF (V_Counter > 1) ASSIGN V_List = V_List + " " + V_CurName

  V_Counter = V_Counter + 1
  ```
 
* **Abordagem 2: Comando `GROUP` (Iteração Interna por Registro)**
  * O comando `GROUP` permite executar uma lista de comandos sequenciais para cada registro da tabela ativa, de forma linear e performática, sem a necessidade de chamar scripts externos ou gerenciar contadores manualmente para mover o ponteiro. Utilize a tool `{tools_names.get("mcp_get_acl_command_or_function_details", "Get_ACL_Command_or_Function_Details")}` (HREF: r_group.htm) para entender melhor como usar o comando `GROUP`.
  * **RESTRIÇÃO:** O comando `ACCEPT` **não pode ser usado dentro de `GROUP`**.
 
### 6. Input do Usuário em Execução Local
 
#### 6.1 `ACCEPT` — Input de texto aberto (string)
 
* Sintaxe: `ACCEPT "Mensagem" TO v_nome_variavel`
* Abre uma caixa de diálogo interativa. O valor é sempre armazenado como variável **character**.
* Permite múltiplos inputs em um único comando, separados por vírgula:
  ```aclscript
  ACCEPT "Informe a data início:" TO v_inicio; "Informe a data fim:" TO v_fim
  ```
* Pode exibir dropdown de itens do projeto com `FIELDS "xf"` (tabelas), `FIELDS "N"` (campos numéricos), etc.
* **RESTRIÇÃO CRÍTICA:** `ACCEPT` **não pode ser usado dentro do comando `GROUP`**.
* `ACCEPT` **não é seguro para senhas** — use o comando `PASSWORD` para isso.
* `ACCEPT` **não funciona em Robots** (execução agendada em servidor) — use a tag de cabeçalho `//PARAM` nesses casos.
 
#### 6.2 Tag de cabeçalho `//PARAM` — Input via cabeçalho analítico (para Robots)
 
* Usada dentro de um bloco `COMMENT ... END` no cabeçalho do script.
* **Não abre caixa de diálogo** em execução local. Para testes locais, o valor deve ser atribuído manualmente com o operador morsa (`:=`), ao terminar o parâmetro:
  ```aclscript
  COMMENT
  //ANALYTIC TYPE ANALYSIS Descrição do script
  //PARAM v_data_inicio "Informe a data de início:" := `20250209`
  END
  ```
 
#### 6.3 `PASSWORD` — Input de senha (sempre abre caixa de diálogo em execução local)
 
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
  COMMENT Em execução local
  PASSWORD 1 "Informe sua senha SAP:"
  ACCESSDATA64 CONNECTOR NAME "SAP" USER "usuario" PASSWORD 1 TO "Tabela.FIL" ...
  ```

  ```aclscript
  //ANALYTICS TYPE ANALYSIS Processamento de Dados Contábeis
  //PASSWORD 1 "Informe a senha SAP:"
  
  COMMENT Em execução no Robots
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
  ACCEPT "Informe o servidor SAP:" TO V_Server;"Informe o Client SAP:" TO V_Client; "Informe a linguagem do SAP:" TO V_Language; "Informe o número da instância" TO V_Inst
  PASSWORD 1 "Senha SAP:"
  ACCESSDATA64 CONNECTOR NAME "SAP" USER "meu_usuario" PASSWORD 1 TO "T001.FIL" CHARMAX 50 MEMOMAX 100 SOURCE(server=V_Server;client=V_Client;language=V_Language;instancenumber=V_Inst;variablestringlength=256;TemporaryWorkingDirectory=Default)
    SQL_QUERY(
      SELECT * FROM T001
    ) END_QUERY
  ```
 
### 8. Organização de Projetos ACL (Boas Práticas do Fabricante)
 
> **Diretiva opcional:** Esta seção descreve o padrão recomendado pelo fabricante para projetos ACL. Siga-o ao sugerir estruturas de projeto, mas respeite a organização já existente caso o usuário apresente um projeto com estrutura diferente.
 
Projetos ACL bem estruturados são divididos em múltiplos scripts, cada um com responsabilidade única. O script inicial chama os demais em sequência usando o comando `DO`.
 
#### Padrão de nomenclatura
 
Cada script recebe um **marcador serial** como prefixo (ex: `S00`, `S01`, ...) seguido de um nome descritivo. Exemplos de nome para o script inicial: `main`, `inicio`, `init`, `launcher`, `mestre`, `master`.
 
#### Ordem e responsabilidade dos scripts
 
| Script | Responsabilidade |
|---|---|
| `S00_Main` | Recebe as tags de cabeçalho (`//ANALYTIC`, `//PARAM`, `//PASSWORD`, `//RESULT`). Chama todos os scripts seguintes via `DO`. |
| `S01_Variaveis` | Define variáveis constantes usadas pelos demais scripts (datas de corte, caminhos, parâmetros fixos, etc.). |
| `S02_Importacao` | Importa as bases de dados necessárias para a execução atual (`ACCESSDATA`, `IMPORT GRCRESULTS`, etc.). |
| `S03_Preparacao` | Aplica transformações nos dados importados: joins, filtros, computed fields, `CLASSIFY`, `SUMMARIZE`, etc. |
| `S04_Processamento` | Executa o objetivo central do script: testes de auditoria, análises, cruzamentos, identificação de exceções. |
| `S05_Exportacao` | Exporta os resultados produzidos. Em execução via **Robots**, o destino segue a tag `//RESULT FILE` do cabeçalho analítico. Em execução **local**, o destino é definido pelo próprio script. |
 
#### Exemplo de `S00_Main`
 
```aclscript
COMMENT
//ANALYTIC TYPE ANALYSIS Conciliação de Pagamentos
//PARAM v_data_inicio "Data início (AAAA-MM-DD):"
//PARAM v_data_fim "Data fim (AAAA-MM-DD):"
//PASSWORD 1 "Senha SAP:"
//RESULT FILE Resultado_Conciliacao
END
 
COMMENT Script de Variáveis
DO S01_Variaveis

COMMENT Script para Importação de Arquivos ou Tabelas na Nuvem
DO S02_Importacao

COMMENT Script para transformação e ajuste dos dados
DO S03_Preparacao

COMMENT Script que de fato processará os dados segundo regras do teste
DO S04_Processamento

COMMENT Exportação dos resultados
DO S05_Exportacao
```
 
### 9. Variáveis
 
#### 9.1 Criação e tipagem
 
* Variáveis são criadas automaticamente ao receber um valor — não há declaração prévia.
* O tipo é inferido pelo valor atribuído (**tipagem implícita**). Os tipos possíveis são: `Character`, `Numeric`, `Datetime` e `Logical`.
* O comando padrão é `ASSIGN`. A keyword pode ser omitida, mas é boa prática mantê-la:
  ```aclscript
  COMMENT Character
  ASSIGN v_tabela = "AP_Trans"

  COMMENT Numeric
  ASSIGN v_valor_min = 1000

  COMMENT Datetime (backquotes obrigatórios)
  ASSIGN v_data_ini = `20210101`
  
  COMMENT Logical
  ASSIGN v_aprovado = T
  ```
* **`ACCEPT` e `DIALOG` sempre criam variáveis do tipo `Character`**, independentemente do valor — datas e números vindos de input do usuário precisam de conversão antes do uso em expressões tipadas.
 
#### 9.2 Regras de nomenclatura
 
* Máximo de **31 caracteres**
* Apenas caracteres alfanuméricos e `_`; não pode começar com número
* Não usar caracteres não-ASCII (ex: `é`, `ã`) em nomes de variáveis que serão usadas em **substituição de variável** (`%v_nome%`) — causa falha silenciosa
* Nomes são **case-insensitive**: `v_data` e `v_Data` são a mesma variável
* Boa prática: prefixo `v_` (ex: `v_data_inicio`, `v_contador`)
 
#### 9.3 Escopo e ciclo de vida
 
* Variáveis são **globais** — visíveis em todos os scripts do projeto uma vez criadas
* Persistem em memória até o projeto ser fechado
* **Variável permanente:** prefixar o nome com `_` (ex: `_v_config`) faz o valor persistir entre sessões. Não suportada em Robots.
* Para deletar explicitamente:
  ```aclscript
  COMMENT deleta uma variável
  DELETE v_nome OK

  COMMENT deleta todas as variáveis
  DELETE ALL OK
  ```
 
#### 9.4 Substituição de variável (`%v_nome%`)
 
* Quando uma variável `Character` é usada como **argumento de comando** (ex: nome de tabela, caminho de arquivo), o valor precisa ser substituído pelo conteúdo da variável usando `%`:
  ```aclscript
  ASSIGN v_tabela = "AP_Trans"
  
  COMMENT abre a tabela cujo nome está na variável
  OPEN %v_tabela%
  ```
* Sem os `%`, o ACL tentará operar sobre o texto literal `"v_tabela"` — não sobre seu valor.
* Variáveis `Numeric`, `Datetime` e `Logical` **não usam** `%` — são referenciadas diretamente pelo nome.
* Variáveis **também não precisam de `%` quando usadas como parâmetros de funções** — funções recebem a variável diretamente pelo nome:
  ```aclscript
  ALLTRIM(v_tabela)
  ```
 
#### 9.5 Conversão de tipos
 
* `ACCEPT` e `DIALOG` sempre retornam `Character`. Para usar datas ou números vindos de input do usuário em expressões tipadas, converter explicitamente:
  ```aclscript
  COMMENT Character → Datetime
  CTOD(v_data_char)

  COMMENT Character → Numeric
  VALUE(v_numero_char, 2)
  ```
 
#### 9.6 Variáveis de sistema
 
* Alguns comandos criam variáveis de sistema automaticamente após execução. Exemplos:
  * `COUNT` → `COUNT1` (total de registros contados)
  * `FIND` → `FOUND` (lógica: T se encontrou, F se não)
* Essas variáveis podem ser usadas imediatamente após o comando que as gerou:
  ```aclscript
  COUNT
  COMMENT encerra o script se a tabela estiver vazia
  ESCAPE IF COUNT1 = 0
  ```
"""
