def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix" in resp.data.decode()


def test_detail(client):
    client.post(
        "/tickets/new",
        data={"title": "演示工单", "room": "A区101", "description": "演示：灯坏了"},
    )
    resp = client.get("/tickets/1")
    assert resp.status_code == 200
    assert "演示工单" in resp.data.decode()
    assert "A区101" in resp.data.decode()
    assert "演示：灯坏了" in resp.data.decode()


def test_create(client):
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "测试工单" in resp.data.decode()
