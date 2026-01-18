from fastapi import status
from httpx import AsyncClient


async def test_root_returns_index_html(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "Todo" in response.text
