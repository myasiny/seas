from __future__ import print_function, division

from flask import Flask, request
from flask_restful import Resource, Api


from random import random

app = Flask(__name__)
api = Api(app)

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



api.add_resource(printHello,"/hello")
api.add_resource(getRandomNumbers, "/random")
api.add_resource(mainPage,"/")

if __name__ == "__main__":
    app.run(host = "localhost", port = 8888)
