from htmy import Component, Renderer


async def render_html(page: Component) -> str:
    return await Renderer().render(page)
