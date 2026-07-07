def create_rest_integration(client, auth_headers, failure_mode=None):
    payload = {
        "name": "API REST de clientes",
        "type": "REST",
        "url": "https://api.exemplo.local/clientes",
        "status": "ativa",
        "description": "Integração REST simulada para testes.",
        "failure_mode": failure_mode,
    }
    return client.post("/integrations", json=payload, headers=auth_headers)


def test_criar_integracao(client, auth_headers):
    response = create_rest_integration(client, auth_headers)

    assert response.status_code == 201
    assert response.json()["type"] == "REST"


def test_listar_integracoes(client, auth_headers):
    create_rest_integration(client, auth_headers)

    response = client.get("/integrations", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_testar_integracao_rest(client, auth_headers):
    created = create_rest_integration(client, auth_headers).json()

    response = client.get(f"/integrations/{created['id']}/test", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["integration_type"] == "REST"


def test_simular_erro_500(client, auth_headers):
    created = create_rest_integration(client, auth_headers, failure_mode="server_error").json()

    response = client.get(f"/integrations/{created['id']}/test", headers=auth_headers)

    assert response.status_code == 500


def test_historico_de_testes(client, auth_headers):
    created = create_rest_integration(client, auth_headers).json()
    client.get(f"/integrations/{created['id']}/test", headers=auth_headers)

    response = client.get(f"/integrations/{created['id']}/tests", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()[0]["status_code"] == 200
