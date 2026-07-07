def test_testar_integracao_soap(client, auth_headers):
    payload = {
        "name": "SOAP Consulta Cliente",
        "type": "SOAP",
        "url": "https://soap.exemplo.local/clientes",
        "status": "ativa",
        "description": "Integração SOAP simulada para demonstrar XML.",
    }
    created = client.post("/integrations", json=payload, headers=auth_headers).json()

    response = client.get(f"/integrations/{created['id']}/test", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["integration_type"] == "SOAP"
    assert body["response_payload"]["children"]["Status"] == "Ativo"
