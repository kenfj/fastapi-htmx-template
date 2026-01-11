import pytest
from htmy.html import section
from inline_snapshot import snapshot

from ui.components import app_layout
from utils import render_html


@pytest.mark.asyncio
async def test_app_layout_default():
    html = await render_html(app_layout([section("Hello, world!")]))
    assert html == snapshot("""\
<!DOCTYPE html><html lang="en">
<head >
<title >App</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
<link rel="stylesheet" href="/static/style.css"/>
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-sse@2.2.4" integrity="sha384-A986SAtodyH8eg8x8irJnYUk7i9inVQqYigD6qZ9evobksGNIXfeFvDwLSHcp31N" crossorigin="anonymous"></script>
<script src="/static/app.js"></script>
</head>
<body >
<main class="container">
<section >
Hello, world!
</section>
</main>
<footer class="container">
© 2025 My Todo App
<p >This page was rendered by <code >htmy</code></p>
</footer>
</body>
</html>\
""")
