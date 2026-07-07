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

## Como instalar

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
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
