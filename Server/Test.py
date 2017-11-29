from requests import put, get, post, delete

put("http://localhost:8888/todos/todo1", data={"data":"Remember the milk"}).json()
put("http://localhost:8888/todos/todo2", data={"data":"2 loaf of bread"}).json()