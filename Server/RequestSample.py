from requests import put, get, post, delete
from DatabaseAPI import *
"""
put("http://localhost:8888/todos/todo1", data={"data":"Remember the milk"}).json()
put("http://localhost:8888/todos/todo2", data={"data":"2 loaf of bread"}).json()
"""
"""
addOrganization("http://localhost:8888", "Istanbul Sehir University")
addUser("http://localhost:8888", "Istanbul Sehir University", "213962062", "Fatih Cagatay", "Gulmez", "fatihgulmez", "12345",role="student")
addUser("http://localhost:8888", "Istanbul Sehir University", "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345", role="student")
addUser("http://localhost:8888", "Istanbul Sehir University", "213944444", "Ali Emre", "Oz", "alioz", "12345", role="student")
addUser("http://localhost:8888", "Istanbul Sehir University", "000000000", "Admin", "Admin", "admin", "12345", role="Admin")
"""

print signIn("http://localhost:8888", "Istanbul Sehir University", "admin", "1234")
print signIn("http://localhost:8888", "Istanbul Sehir University", "admin", "12345")