#from __future__ import print_function, division

from flask import Flask, request
from flask_restful import Resource, Api
from Models import MySQLdb
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
db = MySQLdb("TestDB", app)

# Adds Organization to Database
class signUpOrganization(Resource):
    def get(self):
        return db.execute("select * from Organizations")

    def put(self):
        db.execute("CREATE TABLE IF NOT EXISTS Organizations "
                   "( "
                   "Name CHAR(40) NOT NULL, "
                   "ID INT NOT NULL AUTO_INCREMENT, "
                   "PRIMARY KEY (ID),"
                   "UNIQUE (Name) )")
        org = request.form["data"]
        org = org.replace(" ", "_").lower()
        db.execute("CREATE TABLE IF NOT EXISTS %s ("
                   "Domain INT NOT NULL,"
                   "ID INT NOT NULL,"
                   "Role CHAR(10) NOT NULL,"
                   "Name CHAR(25) NOT NULL, "
                   "Surname CHAR(20) NOT NULL,"
                   "Username CHAR(25) NOT NULL,"
                   "Password CHAR(25) NOT NULL,"
                   "PRIMARY KEY (ID),"
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID) "
                   ")" %org)
        try:
            db.execute("INSERT INTO Organizations ( Name ) VALUES ( '%s' )" % org)
        except:
            print "Integrity Error"
            pass

# Adds new users to Database of organization
class signUpUser(Resource):
    def get(self, organization):

        org = db.execute("select Name from Organizations where Name = (%s)" %organization).pop(0)[0].replace(" ", "_").lower()
        command = "select * from %s" %org
        return db.execute(command)

    def put(self, organization):
        try:
            domain = db.execute("SELECT ID FROM Organizations WHERE Name = ('"+ organization.replace(" ", "_").lower() +"')")
            print domain
            command = "Insert into %s(Domain, ID, Role, Name, Surname, Username, Password) values('%d', %s, '%s', '%s', '%s', '%s', '%s')" \
                      %(organization.replace(" ", "_").lower(),
                       domain ,
                       request.form["ID"],
                       request.form["Role"],
                       request.form["Name"],
                       request.form["Surname"],
                       request.form["Username"],
                       request.form["Password"])
            db.execute(command)
            return True
        except :
            print "Integrity Error"
            return False

# Checks user credentials.
class signInUser(Resource):
    def get(self, organization, user):
        org = db.execute("select Name from Organizations where Name = (%s)" %organization).pop(0)[0].replace(" ",
                                                                                                        "_").lower()
        try:
            passwd = db.execute("select Password from %s where Username = (%s)" %(org,user)).pop(0)[0]
        except IndexError:
            return None
        if passwd == request.form["Password"]:
            return db.execute("select Username, Name, Surname, ID, Role from %s where Username=(%s)" %(org, request.form["Username"]))
        else:
            return None



api.add_resource(signUpUser, "/organizations/<string:organization>")
api.add_resource(signUpOrganization, "/organizations")
api.add_resource(signInUser, "/organizations/<string:organization>/<string:user>")

if __name__ == "__main__":
    app.run(host = "localhost", port = 8888)
