#from __future__ import print_function, division

from flask import Flask, request
from flask_restful import Resource, Api
from Models import MySQLdb, Password, Credential

app = Flask(__name__)
api = Api(app)

db = MySQLdb("TestDB", app)

# Adds Organization to Database

class testConnection(Resource):
    def get(self):
        return True

class signUpOrganization(Resource):
    def get(self, username, password):
        user = Credential(username, password)
        user.checkPassword()
        return db.execute("select * from Organizations")

    def put(self, username, password):

        org = request.form["data"]
        org = org.replace(" ", "_").lower()
        db.execute("CREATE TABLE IF NOT EXISTS %s_members ("
                   "Domain INT NOT NULL,"
                   "ID INT NOT NULL,"
                   "Role INT NOT NULL,"
                   "Name CHAR(25) NOT NULL, "
                   "Surname CHAR(20) NOT NULL,"
                   "Username CHAR(25) NOT NULL,"
                   "Password CHAR(128) NOT NULL,"
                   "Email CHAR(60) ,"
                   "Department Char(60),"
                   "PRIMARY KEY (ID),"
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID), "
                   "FOREIGN KEY (Role) REFERENCES roles(ID)"
                   ")" %org)

        db.execute("CREATE TABLE IF NOT EXISTS %s_courses ("
                   "Domain INT NOT NULL,"
                   "ID INT NOT NULL, "
                   "isActive BOOLEAN DEFAULT True, "
                   "Name CHAR(25) NOT NULL, "
                   "PRIMARY KEY (ID),"
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID),"
                   "UNIQUE (Name) "
                   ")" % org)

        db.execute("CREATE TABLE IF NOT EXISTS %s_lecturers ("
                   "Domain INT NOT NULL,"
                   "Lecturer_ID INT NOT NULL,"
                   "Course_ID INT NOT NULL, "
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID),"
                   "FOREIGN KEY (Lecturer_ID) REFERENCES %s_members(ID),"
                   "FOREIGN KEY (Course_ID) REFERENCES %s_courses(ID)"
                   ")" %(org, org, org))
        db.execute("ALTER TABLE %s_lecturers ADD UNIQUE Index(Lecturer_ID, Course_id)" %org)

        db.execute("CREATE TABLE IF NOT EXISTS %s_registrations ("
                   "Domain INT NOT NULL,"
                   "Student_ID INT NOT NULL,"
                   "Course_ID INT NOT NULL, "
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID),"
                   "FOREIGN KEY (Student_ID) REFERENCES %s_members(ID),"
                   "FOREIGN KEY (Course_ID) REFERENCES %s_courses(ID)"
                   ")" % (org, org, org))

        db.execute("ALTER TABLE %s_registrations ADD UNIQUE Index(Student_ID, Course_id)" % org)

        db.execute("CREATE TABLE IF NOT EXISTS %s_roles ("
                   "Domain INT NOT NULL,"
                   "UserID INT NOT NULL,"
                   "RoleID INT NOT NULL,"
                   "FOREIGN KEY (Domain) REFERENCES Organizations (ID),"
                   "FOREIGN KEY (UserID) REFERENCES %s_members (ID),"
                   "FOREIGN KEY (RoleID) REFERENCES roles (ID))" %(org, org))

        db.execute("ALTER TABLE %s_roles ADD UNIQUE Index(Domain, UserID, RoleID)" % org)

        try:
            db.execute("INSERT INTO Organizations ( Name ) VALUES ( '%s' )" % org)
        except:
            print "Integrity Error"
            pass

# Adds new users to Database of organization
class signUpUser(Resource):
    def get(self, username, password, organization):
        org = db.execute("select Name from Organizations where Name = (%s)" %organization)[0].replace(" ", "_").lower()
        command = "select * from '%s'" %org
        return db.execute(command)

    def put(self, username, password, organization):
        try:
            domain = db.execute("SELECT ID FROM Organizations WHERE Name = ('"+ organization.replace(" ", "_").lower() +"')")[0]
            command = "Insert into %s_members(Domain, ID, Role, Name, Surname, Username, Password, Email, Department) " \
                      "values('%d', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                      %(organization.replace(" ", "_").lower(),
                        domain ,
                        request.form["ID"],
                        db.execute("SELECT ID FROM roles WHERE Name = '%s'" %request.form["Role"])[0],
                        request.form["Name"],
                        request.form["Surname"],
                        request.form["Username"],
                        Password().hashPassword(request.form["Password"]),
                        request.form["Email"],
                        request.form["Department"]
                        )
            db.execute(command)

            db.execute("INSERT INTO %s_roles (Domain, UserID, RoleID) values ( '%s', '%s', '%s')" %(
                organization.replace(" ", "_").lower(),
                db.execute("SELECT ID FROM organizations WHERE Name = '%s'" % organization.replace(" ", "_").lower())[0],
                db.execute("SELECT ID FROM %s_members WHERE Username = '%s'" % (organization.replace(" ", "_").lower()
                                                                                , request.form["Username"]))[0],
                db.execute("SELECT ID FROM roles WHERE Name = '%s'" % request.form["Role"])[0]
            ))
            return True
        except:
            print "Duplicate Entry"
            return False


# Checks user credentials.
class signInUser(Resource):
    def get(self, organization, username):
        org = db.execute("SELECT Name FROM Organizations WHERE Name = '"+ organization.replace(" ", "_").lower() +"'")[0]
        try:
            passwd = db.execute("select Password from %s_members where Username = '%s'" % (org, username))[0]
            if Password().verify_password_hash(request.form["Password"] ,passwd):
                rtn = list(db.execute("select Username, Name, Surname, ID, Role, Email, Department "
                                      "from %s_members where Username=('%s')" % (org, request.form["Username"])))
                rtn[4] = db.execute("SELECT Name FROM roles WHERE ID = '%s'" %rtn[4])[0]
                rtn.append(org)
                return rtn
            else:
                return "Wrong Password"
        except IndexError:
            return None
        except TypeError:
            return "Wrong Username!"


class changePassword(Resource):
    def put(self, organization, username, password):

        pass


api.add_resource(signUpUser, "/organizations/<string:organization>")
api.add_resource(signUpOrganization, "/organizations")
api.add_resource(signInUser, "/organizations/<string:organization>/<string:username>")
api.add_resource(changePassword, "/organizations/<string:organization>/edit_password")
api.add_resource(testConnection, "/")

if __name__ == "__main__":
    app.run(host = "10.50.81.24", port = 8888)
