from playwright.async_api import Page, expect

from tests.e2e.config import BASE_URL


async def test_todo_home_empty(page: Page):
    await page.goto(f"{BASE_URL}/")

    await expect(page.locator("text=No todos.")).to_be_visible()
    await expect(page.locator("#completed-count")).to_have_text("0 / 0 Completed")


async def test_add_todo(page: Page):
    await page.goto(f"{BASE_URL}/")

    await page.get_by_role("button", name="Add Todo").click()

    await page.fill('input[name="title"]', "Test")
    await page.fill('textarea[name="description"]', "desc")
    await page.click('button[type="submit"]')

    await expect(page.locator(".todo-row")).to_be_visible()
    await expect(page.locator(".todo-row span")).to_have_text(["Test", "desc", "🗑️"])
    await expect(page.locator("#completed-count")).to_have_text("0 / 1 Completed")


async def test_complete_todo(page: Page):
    await page.goto(f"{BASE_URL}/")
    await page.get_by_role("button", name="Add Todo").click()

    await page.fill('input[name="title"]', "Test")
    await page.fill('textarea[name="description"]', "desc")
    await page.click('button[type="submit"]')

    await expect(page.locator("#completed-count")).to_have_text("0 / 1 Completed")

    checkbox = page.locator(".todo-row input[type=checkbox]")
    await checkbox.check()
    await expect(page.locator("#completed-count")).to_have_text("1 / 1 Completed")


async def test_delete_todo(page: Page):
    await page.goto(f"{BASE_URL}/")
    await page.get_by_role("button", name="Add Todo").click()

    await page.fill('input[name="title"]', "Test")
    await page.fill('textarea[name="description"]', "desc")
    await page.click('button[type="submit"]')

    await expect(page.locator("#completed-count")).to_have_text("0 / 1 Completed")

    delete_btn = page.locator(".todo-row span[aria-label=Delete]")
    await delete_btn.click()

    await expect(page.locator(".todo-row")).to_have_count(0)
    await expect(page.locator("#completed-count")).to_have_text("0 / 0 Completed")
