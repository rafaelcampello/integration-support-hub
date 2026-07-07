# Integration Support Hub

Plataforma educacional e profissional para simular suporte a integrações REST/SOAP com autenticação JWT, documentação Swagger, logs técnicos, SQLite e histórico de testes.

## Objetivo

Este projeto foi criado para portfólio de uma vaga de Assistente de Suporte e Integrações. A proposta é demonstrar, de forma prática e didática, como investigar integrações entre sistemas, autenticar chamadas, testar cenários de sucesso e erro, consultar logs e entender fluxos REST/SOAP.

## Tecnologias

- Python 3.14.6
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- PyJWT
- Uvicorn
- HTTPX/Requests
- pytest
- Jupyter Notebook
- Swagger/OpenAPI
- Postman

## Funcionalidades

- Login com usuário demo `admin` e senha `admin123`
- Token JWT para proteger endpoints principais
- Cadastro, listagem e consulta de integrações
- Teste de integração REST simulada
- Teste de integração SOAP simulada com XML convertido para JSON
- Cenários controlados de erro: 400, 401, 403, 404, 500 e timeout 504
- Logs em arquivo em `logs/app.log`
- Eventos técnicos salvos no banco
- Histórico de testes de integração
- Swagger automático em `/docs`
- Collection do Postman em `postman/`
- Notebook explicativo em `notebooks/`

## Arquitetura resumida

```text
app/
  main.py                  # Inicialização da API, banco e usuário padrão
  auth.py                  # JWT, senha e dependências de autenticação
  database.py              # Conexão SQLite e sessões SQLAlchemy
  models.py                # Tabelas users, integrations, integration_tests e technical_logs
  schemas.py               # Contratos Pydantic usados pela API
  routers/                 # Rotas HTTP por tema
  services/                # Regras de negócio e simulações REST/SOAP
  utils/                   # Utilitários de XML
```

## Primeiros passos no Windows

Este passo a passo foi escrito para quem está começando do zero em um computador Windows.

### 1. Instalar os programas necessários

Instale estes programas antes de clonar o projeto:

- **Python 3.14.6**: https://www.python.org/downloads/
- **Git for Windows**: https://git-scm.com/download/win
- **Visual Studio Code**: https://code.visualstudio.com/
- **Postman** opcional, para testar a API por interface gráfica: https://www.postman.com/downloads/

Durante a instalação do Python, marque a opção **Add python.exe to PATH**. Durante a instalação do Git, mantenha a opção que permite usar o Git pelo terminal, normalmente chamada **Git from the command line and also from 3rd-party software**.

### 2. Verificar se Python e Git estão no PATH

Depois de instalar, feche e abra novamente o PowerShell. Isso faz o Windows recarregar o PATH.

Rode:

```powershell
python --version
git --version
```

O esperado é algo parecido com:

```text
Python 3.14.6
git version 2.x.x
```

Se aparecer mensagem dizendo que `python` ou `git` não é reconhecido, o programa não foi adicionado ao PATH. Nesse caso:

1. Abra o menu Iniciar e pesquise por **Editar as variáveis de ambiente do sistema**.
2. Clique em **Variáveis de Ambiente**.
3. Em **Variáveis do usuário**, selecione **Path** e clique em **Editar**.
4. Adicione os caminhos do Python e do Git, se eles não existirem.

Caminhos comuns do Python:

```text
C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python314\
C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python314\Scripts\
```

Caminhos comuns do Git:

```text
C:\Program Files\Git\cmd\
C:\Program Files\Git\bin\
```

Depois disso, feche e abra o PowerShell novamente e repita:

```powershell
python --version
git --version
```

### 3. Clonar o repositório

Escolha uma pasta onde você guarda seus projetos. Exemplo usando `Documents`:

```powershell
cd $HOME\Documents
git clone https://github.com/rafaelcampello/integration-support-hub.git
cd integration-support-hub
```

Se você usa o Visual Studio Code, abra a pasta do projeto com:

```powershell
code .
```

Se o comando `code .` não funcionar, abra o VS Code manualmente, pressione `Ctrl+Shift+P`, procure por **Shell Command: Install 'code' command in PATH** ou abra a pasta pelo menu **File > Open Folder**.

## Como instalar o projeto

Todos os comandos abaixo devem ser executados dentro da pasta `integration-support-hub`.

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
venv\Scripts\activate
```

Quando ativar corretamente, o terminal deve mostrar `(venv)` no começo da linha.

Atualize o `pip`:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Verifique se o `uvicorn` foi instalado:

```powershell
python -m pip show uvicorn
```

No Linux/Mac, a ativação do ambiente virtual seria:

```bash
source venv/bin/activate
```

Crie o arquivo `.env` a partir do exemplo:

No Windows PowerShell:

```bash
Copy-Item .env.example .env
```

No Linux/Mac:

```bash
cp .env.example .env
```

Para estudo local, você pode usar os valores do `.env.example`. A chave `SECRET_KEY` é apenas uma chave de demonstração; em produção ela deveria ser trocada por uma string longa, aleatória e privada.

## Como rodar

```bash
python -m uvicorn app.main:app --reload
```

Acesse:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Fluxo REST + SOAP + JWT

1. Faça login em `POST /auth/login`.
2. Copie o `access_token` retornado.
3. Use o token como `Bearer Token` nos endpoints protegidos.
4. Cadastre uma integração REST ou SOAP em `POST /integrations`.
5. Execute `GET /integrations/{id}/test`.
6. Se a integração for SOAP, a aplicação monta XML, simula uma resposta XML e devolve JSON padronizado.
7. Consulte `GET /integrations/{id}/tests` e `GET /logs` para análise técnica.

Exemplo de login:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Exemplo de integração SOAP:

```json
{
  "name": "SOAP Consulta Cliente",
  "type": "SOAP",
  "url": "https://soap.exemplo.local/clientes",
  "status": "ativa",
  "description": "Integração SOAP simulada para demonstrar XML."
}
```

## Postman

Importe a collection:

```text
postman/Integration_Support_Hub.postman_collection.json
```

Depois execute a requisição `Login`. A collection salva o token em uma variável e usa esse token nas demais chamadas.

## Jupyter Notebook

O projeto inclui um notebook de estudo em:

```text
notebooks/01_estudo_do_projeto.ipynb
```

Para abrir o notebook no Windows, primeiro confirme que você está na pasta do projeto e com o `venv` ativado:

```powershell
cd $HOME\Documents\integration-support-hub
venv\Scripts\activate
```

Depois instale as dependências, caso ainda não tenha feito:

```powershell
python -m pip install -r requirements.txt
```

Abra o Jupyter Notebook com:

```powershell
python -m notebook
```

Se o comando acima não abrir, use:

```powershell
python -m jupyter notebook
```

O navegador deve abrir automaticamente. Na tela do Jupyter, entre na pasta `notebooks/` e clique em `01_estudo_do_projeto.ipynb`.

Para encerrar o Jupyter, volte ao terminal onde ele está rodando e pressione `Ctrl+C`. Se ele perguntar se deseja parar o servidor, confirme com `y` e `Enter`.

## Testes automatizados

```bash
python -m pytest
```

Os testes cobrem login válido, login inválido, acesso sem token, cadastro e listagem de integrações, teste REST, teste SOAP e simulação de erro. O projeto foi validado localmente com Python 3.14.6.

## Solução de problemas

Se aparecer `No module named uvicorn`, o `uvicorn` não foi instalado dentro do ambiente virtual ativo. Com o `venv` ativado, rode:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip show uvicorn
```

Depois inicie a API com:

```bash
python -m uvicorn app.main:app --reload
```

## Relação com suporte e integrações

O projeto simula situações comuns em suporte técnico: validar autenticação, reproduzir falhas, diferenciar erro de cliente e erro de servidor, analisar logs, consultar histórico e traduzir respostas SOAP/XML para um formato JSON mais simples de investigar.

## Melhorias futuras

- Adicionar Alembic para migrations
- Criar níveis de permissão mais completos
- Enviar métricas para Prometheus ou Grafana
- Adicionar filas para testes assíncronos
- Incluir dashboard web para acompanhamento dos testes
- Expandir os cenários SOAP com WSDL real
