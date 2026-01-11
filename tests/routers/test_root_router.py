from fastapi import status


def test_root_returns_index_html(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "Todo" in response.text
