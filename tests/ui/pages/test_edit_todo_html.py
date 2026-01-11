from inline_snapshot import snapshot


def test_edit_todo(client):
    todo = {"title": "Test", "description": "desc", "completed": False}
    response = client.post("/todos/add", data=todo, follow_redirects=False)
    todo_id = response.headers["X-Created-Todo-ID"]

    response = client.get(f"/todos/{todo_id}/edit")

    assert response.text == snapshot("""\
<!DOCTYPE html><html lang="en">
<head >
<title >Edit Todo</title>
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
<h1 >Edit Todo</h1>
<form method="post" action="/todos/1/edit">
<fieldset >
<label htmlFor="title">
Title
</label>
<input type="text" name="title" id="title" value="Test" required="true" placeholder="Title"/>
<label htmlFor="description">
Description
</label>
<textarea name="description" id="description" placeholder="Description">
desc
</textarea>
<label htmlFor="completed">
Completed
</label>
<input type="checkbox" name="completed" id="completed"/>
</fieldset>
<button type="submit">
Update
</button>
</form>
<a href="/" role="button">Back</a>
</section>
</main>
<footer class="container">
© 2025 My Todo App
<p >This page was rendered by <code >htmy</code></p>
</footer>
</body>
</html>\
""")
