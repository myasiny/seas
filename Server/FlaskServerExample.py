#from __future__ import print_function, division

from flask import Flask, request
from flask_restful import Resource, Api

from Models import DataBase
from random import random

app = Flask(__name__)
api = Api(app)
db = DataBase("TestDB.db")
db.createTable("TODOS", ID="Char(10)", Name="Char(50)")

class printHello(Resource):
    def get(self):
        return "hello world"

class getRandomNumbers(Resource):
    def get(self):
        a = []
        for i in range(50):
            a.append(int(random()*10))
        return a

class mainPage(Resource):
    def get(self):
        return "WELCOME"

class itemGetPutFromDB(Resource):
    def get(self, id):
        return db.execute("select * from TODOS where ID = ?", id)

    def put(self, id):
        db.execute("Insert into TODOS(ID, Name) values(?,?)", (id, request.form["data"]))
        return (id, request.form["data"])

class getTodos(Resource):
    def get(self):
        return db.execute("select * from TODOS")

api.add_resource(getTodos, "/todos")
api.add_resource(itemGetPutFromDB, "/todos/<string:id>")
api.add_resource(printHello,"/hello")
api.add_resource(getRandomNumbers, "/random")
api.add_resource(mainPage,"/")

if __name__ == "__main__":
    app.run(host = "localhost", port = 8888)
