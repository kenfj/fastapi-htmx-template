from bs4 import BeautifulSoup
from inline_snapshot import snapshot


def test_todo_home_empty(client):
    response = client.get("/")

    assert response.text == snapshot("""\
<!DOCTYPE html><html lang="en">
<head >
<title >Todo List</title>
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
<h1 >Todo List</h1>
<div style="display:flex;">
<p id="completed-count" hx-ext="sse" sse-connect="/todos/completed_count/stream" sse-swap="update">0 / 0 Completed</p>
<a href="/todos/add" role="button" style="margin-left:auto;">Add Todo</a>
</div>
</section>
<section >
<p >No todos.</p>
</section>
</main>
<footer class="container">
© 2025 My Todo App
<p >This page was rendered by <code >htmy</code></p>
</footer>
</body>
</html>\
""")


def test_todo_home_with_data(client):
    todo = {"title": "Test", "description": "desc", "completed": False}
    client.post("/todos/add", data=todo)
    response = client.get("/")
    pretty_html = BeautifulSoup(response.text, "html.parser").prettify()

    assert pretty_html == snapshot("""\
<!DOCTYPE html>
<html lang="en">
 <head>
  <title>
   Todo List
  </title>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" rel="stylesheet"/>
  <link href="/static/style.css" rel="stylesheet"/>
  <script crossorigin="anonymous" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js">
  </script>
  <script crossorigin="anonymous" integrity="sha384-A986SAtodyH8eg8x8irJnYUk7i9inVQqYigD6qZ9evobksGNIXfeFvDwLSHcp31N" src="https://cdn.jsdelivr.net/npm/htmx-ext-sse@2.2.4">
  </script>
  <script src="/static/app.js">
  </script>
 </head>
 <body>
  <main class="container">
   <section>
    <h1>
     Todo List
    </h1>
    <div style="display:flex;">
     <p hx-ext="sse" id="completed-count" sse-connect="/todos/completed_count/stream" sse-swap="update">
      0 / 1 Completed
     </p>
     <a href="/todos/add" role="button" style="margin-left:auto;">
      Add Todo
     </a>
    </div>
   </section>
   <section>
    <ul>
     <li class="todo-row">
      <input hx-post="/todos/1/toggle_completed" hx-swap="outerHTML" hx-target="this" hx-trigger="change" name="completed" style="margin-right:0.5em;" type="checkbox"/>
      <span style="font-weight:bold;">
       Test
      </span>
      <span style="color:gray;">
       desc
      </span>
      <a aria-label="Edit" href="/todos/1/edit" style="text-decoration:none; font-size:1.2em;" tabindex="0" title="Edit">
       ✏️
      </a>
      <span aria-label="Delete" hx-delete="/todos/1" hx-swap="delete swap:1s" hx-target="closest li" style="cursor:pointer; font-size:1.2em;" tabindex="0" title="Delete">
       🗑️
      </span>
     </li>
    </ul>
   </section>
  </main>
  <footer class="container">
   © 2025 My Todo App
   <p>
    This page was rendered by
    <code>
     htmy
    </code>
   </p>
  </footer>
 </body>
</html>
""")
