def test_login_valido_retorna_token(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_invalido_retorna_401(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "senha-errada"})

    assert response.status_code == 401


def test_endpoint_protegido_sem_token_retorna_401(client):
    response = client.get("/integrations")

    assert response.status_code == 401
