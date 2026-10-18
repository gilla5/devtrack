NEW = {"company": "Acme", "role": "Backend Intern", "status": "Applied"}


def test_create_and_list(client, signup):
    signup(client)
    assert client.post("/applications/new", data=NEW).status_code == 302
    assert b"Acme" in client.get("/applications/").data


def test_invalid_form_saves_nothing(client, signup):
    signup(client)
    client.post("/applications/new", data={"company": "", "role": "x", "status": "Applied"})
    assert b"Acme" not in client.get("/applications/").data
    assert b"No applications match" in client.get("/applications/").data


def test_users_cannot_touch_each_others_data(client, signup):
    signup(client, "a@example.com")
    client.post("/applications/new", data=NEW)
    client.post("/logout")
    signup(client, "b@example.com")
    assert client.get("/applications/1/edit").status_code == 404
    assert client.post("/applications/1/delete").status_code == 404
    assert b"Acme" not in client.get("/applications/").data
    client.post("/logout")
    client.post("/login", data={"email": "a@example.com", "password": "password123"})
    assert b"Acme" in client.get("/applications/").data


def test_dashboard_stats_and_zero_safe(client, signup):
    signup(client)
    assert b"0%" in client.get("/").data  # no applications: no division error
    client.post("/applications/new", data=NEW)
    client.post("/applications/new", data={**NEW, "company": "Beta", "status": "Interviewing"})
    html = client.get("/").data.decode()
    assert "<b>2</b>applied" in html and "<b>1</b>interviews" in html and "50%" in html
