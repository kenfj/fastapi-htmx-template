from typing import TYPE_CHECKING

from htmy.html import (
    DOCTYPE,
    Meta,
    body,
    code,
    footer,
    head,
    html,
    link,
    main,
    p,
    script,
    title,
)

from core.constants import (
    HTMX_JS_INTEGRITY,
    HTMX_JS_URL,
    HTMX_SSE_EXT_URL,
    HTMX_SSE_INTEGRITY,
    PICO_CSS_URL,
)

if TYPE_CHECKING:
    from htmy import Component, ComponentType


def app_layout(contents: list[ComponentType], page_title: str = "App") -> Component:
    return (
        DOCTYPE.html,
        html(
            head(
                title(page_title),
                Meta.charset(),
                Meta.viewport(),
                link(rel="stylesheet", href=PICO_CSS_URL),
                link(rel="stylesheet", href="/static/style.css"),
                script(
                    src=HTMX_JS_URL,
                    integrity=HTMX_JS_INTEGRITY,
                    crossorigin="anonymous",
                ),
                script(
                    src=HTMX_SSE_EXT_URL,
                    integrity=HTMX_SSE_INTEGRITY,
                    crossorigin="anonymous",
                ),
                script(src="/static/app.js"),
            ),
            body(
                main(*contents, class_="container"),
                footer(
                    "© 2025 My Todo App",
                    p("This page was rendered by ", code("htmy")),
                    class_="container",
                ),
            ),
            lang="en",
        ),
    )
