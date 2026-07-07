# Arquitetura do Integration Support Hub

## Visão geral

A aplicação foi desenhada para ser simples, didática e próxima de uma rotina de suporte a integrações. O FastAPI expõe endpoints REST, o SQLAlchemy persiste dados em SQLite, o JWT protege endpoints e os serviços simulam integrações externas REST e SOAP.

## Componentes

- `app/main.py`: cria a aplicação, configura o banco e cadastra o usuário padrão.
- `app/auth.py`: concentra hash de senha, geração de JWT e validação de Bearer Token.
- `app/models.py`: define as tabelas da aplicação.
- `app/schemas.py`: define os contratos de entrada e saída da API.
- `app/services/integration_service.py`: executa testes e registra histórico.
- `app/services/soap_service.py`: simula uma integração SOAP usando XML.
- `app/services/troubleshooting_service.py`: salva eventos em arquivo e no banco.
- `app/routers/`: organiza endpoints por domínio.

## Banco de dados

Tabelas principais:

- `users`: usuários que podem autenticar na API.
- `integrations`: integrações REST ou SOAP cadastradas.
- `integration_tests`: histórico de execuções, status, payloads e erros.
- `technical_logs`: eventos técnicos relevantes para troubleshooting.

## Fluxo de teste

1. O usuário autentica em `/auth/login`.
2. O token JWT é enviado no cabeçalho `Authorization`.
3. A rota `/integrations/{id}/test` carrega a integração.
4. O serviço verifica se há um modo de falha configurado.
5. Para REST, devolve um JSON simulado.
6. Para SOAP, monta XML, simula XML de resposta e converte para JSON.
7. O resultado é salvo em `integration_tests`.
8. Eventos importantes são salvos em `technical_logs` e em `logs/app.log`.

## Cenários de troubleshooting

O campo `failure_mode` permite simular:

- `bad_request`: erro 400 por payload inválido.
- `forbidden`: erro 403 por falta de permissão.
- `server_error`: erro 500 no provedor.
- `timeout`: erro 504 por timeout simulado.

Esses cenários ajudam a praticar leitura de logs, interpretação de status HTTP e comunicação técnica de incidentes.
