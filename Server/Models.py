#-*-coding:utf-8-*-

import sqlite3
from flaskext.mysql import MySQL
from passlib.apps import custom_app_context as pwd_context
import sys
sys.path.append("..")

import csv
from Functionality.passwordGenerator import passwordGenerator
from Functionality.sendEmail import sentMail

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
        self.execute(
            "CREATE SCHEMA %s;"
            "USE %s" %(organization, organization)
        )

        if self.execute(
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
                "ID       INT         NOT NULL AUTO_INCREMENT,"
                "NAME     VARCHAR(30) NOT NULL,"
                "CODE     VARCHAR(10) NOT NULL,"
                "isActive BOOLEAN DEFAULT TRUE,"
                "PRIMARY KEY (ID),"
                "UNIQUE (NAME, CODE, isActive)"
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
            "CREATE TABLE exams ("
                "ID INT AUTO_INCREMENT,"
                "Name varchar(255) NOT NULL,"
                "CourseID INT,"
                "Time TIMESTAMP,"
                "PRIMARY KEY (ID),"
                "FOREIGN KEY (CourseID) REFERENCES courses(ID),"
                "UNIQUE (Name),"
                "UNIQUE (Name, Time)"
            ");"
        ) is not None:
            return "Organization Initialized"
        else:
            return "Organization Exists"

    def add_course(self, org, name, code, lecturer_users):
        command = "INSERT INTO %s.courses (NAME, CODE) VALUES ('%s', '%s');" % (org, name, code)
        self.execute(command)
        command = "select ID from %s.courses where CODE = '%s'" % (org, code)
        lecturer_users = lecturer_users.split(":")
        lecture_id = self.execute(command)[0][0]
        command = ""
        if len(lecturer_users) > 0:
            for lecturer in lecturer_users:
                lecturer_id = self.execute("select ID from %s.members where Username = '%s'" % (org, lecturer))[0][0]

                command += "insert into %s.lecturers (LecturerID, CourseID) VALUES ('%s', '%s');" % (org, lecturer_id, lecture_id)
            pass
        self.execute(command)
        return "Course Added!"

    def get_course(self, org, code):
        a = self.execute("SELECT * FROM %s.courses WHERE Code = '%s'" % (org,code))[0]
        lecturer_IDs = self.execute("SELECT LecturerID FROM %s.lecturers WHERE CourseID = '%s'"%(org, a[0]))[0]
        lecturers = ""
        for id in lecturer_IDs:
            lid = self.execute("SELECT Name, Surname FROM %s.members WHERE ID = '%s'" % (org, id))[0]
            lecturers += lid[0] + " " + lid[1] + ":"
        rtn = {
            "ID": a[0],
            "Name": a[1],
            "Code": a[2],
            "Lecturers": lecturers,
            "Participants": self.get_course_participants(a[2], org)
        }
        return rtn

    def register_student(self, studentIDList, courseCode, organization):
        courseID = self.execute("SELECT ID FROM %s.courses WHERE CODE = '%s'" % (organization, courseCode))[0][0]
        for i in studentIDList:
            self.execute("INSERT INTO %s.registrations (StudentID, CourseID) VALUES(%s, %s)" %(organization, i, courseID))
        pass

    def get_course_participants(self, code, organization):
        courseID = self.execute("SELECT ID FROM %s.courses WHERE CODE = '%s'" %(organization, code))[0][0]
        studentIDs = self.execute("SELECT StudentID FROM %s.registrations WHERE CourseID = '%s'" %(organization, courseID))
        print studentIDs
        students = []
        for student in studentIDs:
            info = self.execute("SELECT Name, Surname, ID, Email FROM %s.members WHERE ID = '%s'" % (organization, student[0]))[0]
            students.append(info)

        return students

    def get_lecturer_courses(self, organization, username):
        self.execute("USE %s" % organization)
        command = "SELECT courses.Name, courses.CODE FROM lecturers JOIN courses ON lecturers.CourseID = courses.ID JOIN members ON members.ID = lecturers.LecturerID WHERE members.Username = '%s';" % (username)
        lectureIDs = self.execute(command)
        return lectureIDs

    def get_user_info(self, organization, username):
        return self.execute("SELECT * FROM %s.members WHERE Username='%s'" % (organization, username))[0]

    def execute(self, command):
        # print command
        try:
            self.cursor.execute(command)

            rtn = self.cursor.fetchall()
            self.__commit()
            return rtn

        except:
            return None

    def __commit(self):
        self.db.commit()

    def getOrganization(self):
        pass

    def handle_tr(self, str_):
        str_ = str_.replace("İ", "I").replace("Ç", "C").replace("Ş", "S").replace("Ü", "U").replace("Ö", "O").replace("Ğ",
                                                                                                                    "G")
        str_ = str_.replace("ı", "i").replace("ç", "c").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ğ",
                                                                                                                    "g")
        return str_

    def registerStudentCSV(self, csvDataFile, organization, course, lecturer):
        csvReader = csv.reader(csvDataFile)
        column_names = next(csvReader, None)
        data = list(csvReader)
        auth = []
        reg = []
        for i in data:
            name = self.handle_tr(i[0]).title()
            surname = self.handle_tr(i[1]).title()
            student_number = str(int(float(i[2])))
            mail = i[3]
            department = "UNKNOWN"
            role = 4
            username = name.split()[0].lower() + surname.lower()
            pas = Password()
            password = passwordGenerator(8)
            check = self.execute("Insert into %s.members(ID, Role, Name, Surname, Username, Password, Email, Department) values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(organization, student_number, role, name, surname, username, pas.hashPassword(password), mail, department))
            if check is not None:
                auth.append((name + " " + surname, mail, password))
            reg.append(student_number)
        sentMail(auth, lecturer)
        self.register_student(reg, course, organization)
        return "Done"

    def changePasswordOREmail(self, organization, username, oldPassword, newVal, email=False):
        pas = Password()
        user = self.get_user_info(organization, username)
        password = user[5]
        if pas.verify_password_hash(oldPassword, password):
            if email:
                self.execute(
                    "UPDATE %s.members SET Email='%s' WHERE Username = '%s'" % (organization, newVal, username))
                return "Mail Changed"
            else:
                password = pas.hashPassword(newVal)
                self.execute("UPDATE %s.members SET Password='%s' WHERE Username = '%s'" % (organization, password, username))
                return "Password Changed"
        else:
            return "Not Authorized"

    def delete_student_course(self, organization, course, studentID):
        courseID = self.execute("SELECT ID FROM %s.courses WHERE Code = '%s'" % (organization, course))[0][0]
        command = "DELETE FROM %s.registrations WHERE StudentID = %d AND CourseID = %d" % (organization, int(studentID), int(courseID))
        self.execute(command)
        return None



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
