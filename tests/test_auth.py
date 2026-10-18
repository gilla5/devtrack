def test_register_and_login(client, signup):
    assert signup(client).status_code == 302
    client.post("/logout")
    r = client.post("/login", data={"email": "a@example.com", "password": "password123"})
    assert r.status_code == 302


def test_duplicate_email_rejected(client, signup):
    signup(client)
    client.post("/logout")
    assert b"already registered" in signup(client).data


def test_wrong_password_rejected(client, signup):
    signup(client)
    client.post("/logout")
    r = client.post("/login", data={"email": "a@example.com", "password": "nope"})
    assert b"incorrect" in r.data


def test_private_pages_require_login(client):
    for url in ("/", "/applications/", "/applications/new"):
        r = client.get(url)
        assert r.status_code == 302 and "/login" in r.headers["Location"]
