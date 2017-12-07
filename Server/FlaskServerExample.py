#from __future__ import print_function, division

from flask import Flask, request
from flask_restful import Resource, Api
import datetime
from Models import DataBase
from sqlite3 import IntegrityError as ie

app = Flask(__name__)
api = Api(app)
db = DataBase("TestDB.db")
db.createTable("TODOS", ID="Char(10)", Name="Char(50)")


class signUpOrganization(Resource):
    def get(self):
        return db.execute("select * from Organizations")
    def put(self):
        db.createTable("Organizations", Name="Char(40) Primary Key")
        org = request.form["data"]
        org = org.replace(" ", "_").lower()
        db.createTable(org,
                       ID="Int Primary Key Not Null",
                       Role="Char(10) Not Null",
                       Name="Char(20) Not Null",
                       Surname="Char(20) Not Null",
                       Username="Char(20) Not Null",
                       Password="Char(20) Not Null")
        try:
            db.execute("Insert into Organizations(Name) values (?)", org)
        except ie:
            print "Integrity Error"
            pass

class signUpUser(Resource):
    def get(self, organization):
        org = db.execute("select Name from Organizations where Name = (?)", organization).pop(0)[0].replace(" ", "_").lower()
        command = "select * from %s" %org
        return db.execute(command)

    def put(self, organization):
        try:
            command = "Insert into %s(ID, Role, Name, Surname, Username, Password) values(?, ?, ?, ?, ?, ?)" \
                      %db.execute("select Name from Organizations where Name = (?)", organization).pop(0)[0].replace(" ", "_").lower()
            db.execute(command,
                       request.form["ID"],
                       request.form["Role"],
                       request.form["Name"],
                       request.form["Surname"],
                       request.form["Username"],
                       request.form["Password"])
        except ie:
            print "Integrity Error"

class signInUser(Resource):
    def get(self, organization, user):
        org = db.execute("select Name from Organizations where Name = (?)", organization).pop(0)[0].replace(" ",
                                                                                                        "_").lower()
        passwd = db.execute("select Password from %s where Username = (?)" %org, user).pop(0)[0]
        command = "select Username, Name, Surname, ID, Role from %s where Username=(?)" %org
        if passwd == request.form["Password"]:
            return db.execute(command, request.form["Username"])
        else:
            return "Wrong Password"



api.add_resource(signUpUser, "/organizations/<string:organization>")
api.add_resource(signUpOrganization, "/organizations")
api.add_resource(signInUser, "/organizations/<string:organization>/<string:user>")

if __name__ == "__main__":
    app.run(host = "localhost", port = 8888)
