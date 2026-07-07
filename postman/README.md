# Postman

## Como importar

1. Abra o Postman.
2. Clique em **Import**.
3. Selecione `Integration_Support_Hub.postman_collection.json`.
4. Confirme a importação.

## Como usar

1. Inicie a API com `uvicorn app.main:app --reload`.
2. Execute a requisição `Login`.
3. O script da collection salva o token JWT na variável `token`.
4. Execute as demais requisições protegidas.

Base URL padrão:

```text
http://127.0.0.1:8000
```

Você pode alterar a variável `base_url` na collection se rodar em outra porta.
