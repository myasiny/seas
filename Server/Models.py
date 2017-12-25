import sqlite3
from flaskext.mysql import MySQL
from passlib.apps import custom_app_context as pwd_context

class SqlLiteDB:
    def __init__(self, dbName):
        if ".db" not in dbName:
            self.db = sqlite3.connect(dbName+".db")
        else:
            self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()

    def createTable(self, tableName, **columnNames):
        columns = ""
        for i in columnNames:
            columns += "%s %s, " %(i, columnNames[i])
        columns = columns[0:len(columns)-2]
        tableName = tableName.replace(" ", "_")
        command = "create table if not exists %s (%s)" %(tableName, columns)
        self.cursor.execute(command)
        self.__commit()

    def deleteTable(self, tableName):
        command = "Drop table if exists %s" %(tableName)
        self.cursor.execute(command)

    def execute(self, command, *values):
        rtn = self.cursor.execute(command, values).fetchall()
        self.__commit()
        return rtn

    def __commit(self):
        self.db.commit()


class MySQLdb:

    def __init__(self, dbName, app, user="admin", password="1234"):
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = dbName
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_PORT'] = 8000
        self.name = dbName

        mysql.init_app(app)

        self.db = mysql.connect()
        self.cursor = self.db.cursor()

    def initialize_organization(self, organization):
        try:
            self.execute(
                "CREATE SCHEMA %s;"
                "USE %s" %(organization, organization)
            )

            self.execute(
                "CREATE TABLE roles ("
                    "Role VARCHAR(20),"
                    "ID INT AUTO_INCREMENT,"
                    "PRIMARY KEY (ID),"
                    "UNIQUE (Role)"
                ");"
                "INSERT INTO roles (Role) values ('superuser');"
                "INSERT INTO roles (Role) values ('admin');"
                "INSERT INTO roles (Role) values ('lecturer');"
                "INSERT INTO roles (Role) values ('student');"
                "CREATE TABLE members ("
                    "ID       INT         NOT NULL,"
                    "Role     INT         NOT NULL,"
                    "Name     VARCHAR(25) NOT NULL,"
                    "Surname  VARCHAR(20) NOT NULL,"
                    "Username VARCHAR(25) NOT NULL,"
                    "Password VARCHAR(255) NOT NULL,"
                    "Email    VARCHAR(35) NOT NULL,"
                    "Department VARCHAR(255) NOT NULL,"
                    "PRIMARY KEY (ID),"
                    "FOREIGN KEY (Role) REFERENCES roles (ID),"
                    "UNIQUE (Name, Surname, Username)"
                ");"
                "CREATE TABLE courses ("
                    "ID       INT         NOT NULL,"
                    "NAME     VARCHAR(30) NOT NULL,"
                    "isActive BOOLEAN DEFAULT TRUE,"
                    "PRIMARY KEY (ID)"
                ");"
                "CREATE TABLE registrations ("
                    "StudentID INT NOT NULL,"
                    "CourseID  INT NOT NULL,"
                    "ID        INT AUTO_INCREMENT,"
                    "FOREIGN KEY (StudentID) REFERENCES members (ID),"
                    "FOREIGN KEY (CourseID) REFERENCES courses (ID),"
                    "UNIQUE (StudentID, CourseID),"
                    "PRIMARY KEY (ID)"
                ");"
                "CREATE TABLE lecturers ("
                    "LecturerID INT NOT NULL,"
                    "CourseID   INT NOT NULL,"
                    "ID         INT AUTO_INCREMENT,"
                    "FOREIGN KEY (LecturerID) REFERENCES members (ID),"
                    "FOREIGN KEY (CourseID) REFERENCES courses (ID),"
                    "PRIMARY KEY (ID)"
                ");"
            )
            return "Organization Initialized"
        except self.cursor.ProgrammingError:
            return "Organization Exists"

    def execute(self, command):
        # print command
        try:
            self.cursor.execute(command)

            rtn = self.cursor.fetchone()
            self.__commit()
            return rtn

        except:
            return None

    def __commit(self):
        self.db.commit()

    def getOrganization(self):
        pass

class Password:
    def hashPassword(self, password):
        self.password_hash = pwd_context.encrypt(password, )
        return self.password_hash
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    def verify_password_hash(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

class Credential:
    def __init__(self, username, password, db, org):
        self.username = username
        self.password = password
        self.db = db
        self.org = org
        pass

    def getPassword(self):
        return self.db.execute("SELECT Password FROM %s_members WHERE Username = '%s'" %(self.org, self.username))[0]

    def checkPassword(self):
        return Password().verify_password_hash(Password().hashPassword(self.password), self.getPassword())

    def getRole(self):
        self.db.execute("SELECT Role FROM %s_members WHERE Username='%s'" %(self.org, self.username))

    def getPermissions(self):
        pass






if __name__ == "__main__":
    a = Password("12345")
    a.hashPassword()
    print a.verify_password("1234")