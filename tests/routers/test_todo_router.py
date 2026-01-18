import re

from fastapi import status
from httpx import AsyncClient


def _get_todo_id_by_title(html, title):
    pattern = rf'<li[^>]*>.*?{re.escape(title)}.*?href="/todos/(\d+)/edit"'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return int(match.group(1))
    return None


async def test_todo_home(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "Todo" in response.text


async def test_show_add_todo_form(client: AsyncClient):
    response = await client.get("/todos/add")
    assert response.status_code == status.HTTP_200_OK
    assert "Add Todo" in response.text


async def test_create_todo(client: AsyncClient):
    data = {"title": "api test", "description": "desc", "completed": False}
    response = await client.post("/todos/add", data=data, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/"

    list_resp = await client.get("/")
    assert "api test" in list_resp.text


async def test_show_edit_todo_form(client: AsyncClient):
    data = {"title": "edit me", "description": "desc", "completed": False}
    await client.post("/todos/add", data=data)

    list_resp = await client.get("/")
    todo_id = _get_todo_id_by_title(list_resp.text, "edit me")
    assert todo_id is not None

    response = await client.get(f"/todos/{todo_id}/edit")
    assert response.status_code == status.HTTP_200_OK
    assert "Edit Todo" in response.text


async def test_edit_todo(client: AsyncClient):
    data = {"title": "edit target", "description": "desc", "completed": False}
    await client.post("/todos/add", data=data)

    list_resp = await client.get("/")
    todo_id = _get_todo_id_by_title(list_resp.text, "edit target")
    assert todo_id is not None

    data2 = {"title": "edited", "description": "changed", "completed": True}
    response = await client.post(
        f"/todos/{todo_id}/edit", data=data2, follow_redirects=False
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/"


async def test_toggle_completed_todo(client: AsyncClient):
    data = {"title": "toggle", "description": "desc", "completed": False}
    await client.post("/todos/add", data=data)

    list_resp = await client.get("/")
    todo_id = _get_todo_id_by_title(list_resp.text, "toggle")
    assert todo_id is not None

    response = await client.post(
        f"/todos/{todo_id}/toggle_completed",
        data={"completed": "on"},
        headers={"HX-Request": "true"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "checkbox" in response.text


async def test_htmx_only_missing_header(client: AsyncClient):
    response = await client.post("/todos/1/toggle_completed", data={"completed": "on"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_delete_todo(client: AsyncClient):
    data = {"title": "delete", "description": "desc", "completed": False}
    await client.post("/todos/add", data=data)

    list_resp = await client.get("/")
    todo_id = _get_todo_id_by_title(list_resp.text, "delete")
    assert todo_id is not None

    response = await client.delete(f"/todos/{todo_id}", headers={"HX-Request": "true"})
    assert response.status_code == status.HTTP_200_OK

    get_resp = await client.get(f"/todos/{todo_id}/edit")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


async def test_create_todo_validation(client: AsyncClient):
    data = {"title": "a", "description": "desc", "completed": False}
    response = await client.post("/todos/add", data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert "String should have at least 3 characters" in response.text


async def test_edit_todo_not_found(client: AsyncClient):
    edit_data = {"title": "edited", "description": "changed", "completed": True}
    response = await client.post("/todos/999/edit", data=edit_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
