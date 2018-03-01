#-*-coding:utf-8-*-

import sqlite3
from flaskext.mysql import MySQL
from passlib.apps import custom_app_context as pwd_context
import sys, json, csv, threading
sys.path.append("..")
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
            "CREATE SCHEMA %s;" %organization
        )
        self.execute(
            "USE %s;" %organization
        )
        command_seq = list()

        roleTable = DBTable("roles",
                            [
                                ("Role", "varchar(20)", ""),
                                ("roleID", "INT", "AUTO_INCREMENT")
                            ],
                            uniques=[("Role")],
                            primary_key="RoleID",
                              database=self)

        # command_seq.append(roleTable.get_command())

        memberTable = DBTable("members",
                              [
                                  ("PersonID", "int", "not null"),
                                  ("Role", "int", "not null"),
                                  ("Name", "varchar(255)", "not null"),
                                  ("Surname", "varchar(255)", "not null"),
                                  ("Username", "varchar(255)", "not null"),
                                  ("Password", "varchar(255)", "not null"),
                                  ("Email", "varchar(50)", "not null"),
                                  ("Department", "varchar(255)", "not null")
                              ],
                              primary_key="PersonID",
                              foreign_keys_tuple=[("Role", "roles", "RoleID")],
                              uniques=[("Name", "Surname", "Username"), ("PersonID")],
                              database=self)

        # command_seq.append(memberTable.get_command())

        coursesTable = DBTable("courses",
                               [
                                   ("CourseID", "int", "not null auto_increment"),
                                   ("Name", "varchar(255)", "not null"),
                                   ("Code", "varchar(20)", "not null"),
                                   ("isActive", "boolean", "default true"),
                               ],
                               primary_key="CourseID",
                               uniques=[("Name", "Code", "isActive")],
                              database=self)

        # command_seq.append(coursesTable.get_command())

        regisTable = DBTable("registrations",
                             [
                                 ("StudentID", "int", "not null"),
                                 ("CourseID", "int", "not null"),
                                 ("RegistrationID", "int", "auto_increment")
                             ],
                             foreign_keys_tuple=[
                                 ("StudentID", "members", "PersonID"),
                                 ("courseID", "courses", "CourseID")
                             ],
                             uniques=[
                                 ("StudentID", "CourseID")
                             ],
                             primary_key="RegistrationID",
                              database=self)

        # command_seq.append(regisTable.get_command())

        lecturersTable = DBTable("lecturers",
                                 [
                                     ("LecturerID", "int", "not null"),
                                     ("CourseID", "int", "not null"),
                                     ("LeCorID", "int", "not null auto_increment")
                                 ],
                                 foreign_keys_tuple=
                                 [
                                     ("LecturerID", "members", "PersonID"),
                                     ("CourseID", "courses", "CourseID")
                                 ],
                                 primary_key="LeCorID",
                              database=self)

        # command_seq.append(lecturersTable.get_command())

        examsTable = DBTable("exams",
                             [
                                 ("ExamID", "int", "auto_increment"),
                                 ("Name", "varchar(255)", "not null"),
                                 ("CourseID", "int", ""),
                                 ("Time", "timestamp", ""),
                                 ("Duration", "int", "not null")
                             ],
                             primary_key="ExamId",
                             foreign_keys_tuple=
                             [
                                 ("CourseID", "courses", "CourseID")
                             ],
                             uniques=
                             [
                                 ("Name"),
                                 ("Name", "Time")
                             ],
                              database=self)

        # command_seq.append(examsTable.get_command())

        questionsTable = DBTable("questions",
                                 [
                                     ("QuestionID", "int", "auto_increment"),
                                     ("ExamID", "int", ""),
                                     ("info", "JSON", "")
                                 ],
                                 primary_key="QuestionID",
                                 foreign_keys_tuple=[("ExamID", "exams", "ExamID")],
                              database=self)

        answersTable = DBTable("answers",
                               [
                                   ("answerID", "int", "auto_increment"),
                                   ("examID", "int", "not null"),
                                   ("studentID", "int", "not null"),
                                   ("answers", "JSON", "")
                               ],
                               primary_key="answerID",
                               foreign_keys_tuple=[
                                   ("examID", "exams", "ExamID"),
                                   ("studentID", "members", "PersonID")
                               ],
                               uniques=[
                                   ("examID", "studentID")
                               ],
                               database=self)

        # command_seq.append(questionsTable.get_command())

        self.execute("Insert into roles(Role) values ('superuser'); "
                     "Insert into roles(Role) values ('admin'); "
                     "Insert into roles(Role) values ('lecturer');"
                     "Insert into roles(Role) values ('student');")

    def add_course(self, org, name, code, lecturer_users):
        command = "INSERT INTO %s.courses (NAME, CODE) VALUES ('%s', '%s');" % (org, name, code)
        self.execute(command)
        command = "select CourseID from %s.courses where CODE = '%s'" % (org, code)
        lecturer_users = lecturer_users.split(":")
        lecture_id = self.execute(command)[0][0]
        command = ""
        if len(lecturer_users) > 0:
            for lecturer in lecturer_users:
                lecturer_id = self.execute("select PersonID from %s.members where Username = '%s'" % (org, lecturer))[0][0]

                command += "insert into %s.lecturers (LecturerID, CourseID) VALUES ('%s', '%s');" % (org, lecturer_id, lecture_id)
            pass
        self.execute(command)
        return "Course Added!"

    # todo: fatihgulmez; use JOIN query.
    def get_course(self, org, code):
        a = self.execute("SELECT * FROM %s.courses WHERE Code = '%s'" % (org,code))[0]
        lecturer_IDs = self.execute("SELECT LecturerID FROM %s.lecturers WHERE CourseID = '%s'"%(org, a[0]))[0]
        lecturers = ""
        for id in lecturer_IDs:
            lid = self.execute("SELECT Name, Surname FROM %s.members WHERE PersonID = '%s'" % (org, id))[0]
            lecturers += lid[0] + " " + lid[1] + ":"
        rtn = {
            "ID": a[0],
            "Name": a[1],
            "Code": a[2],
            "Lecturers": lecturers,
            "Participants": self.get_course_participants(a[2], org)
        }
        return rtn

    # todo: fatihgulmez; use JOIN query.
    def register_student(self, studentIDList, courseCode, organization):
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE CODE = '%s'" % (organization, courseCode))[0][0]
        for i in studentIDList:
            self.execute("INSERT INTO %s.registrations (StudentID, CourseID) VALUES(%s, %s)" %(organization, i, courseID))
        pass

    # todo: fatihgulmez; use JOIN query.
    def get_course_participants(self, code, organization):
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE CODE = '%s'" %(organization, code))[0][0]
        studentIDs = self.execute("SELECT StudentID FROM %s.registrations WHERE CourseID = '%s'" %(organization, courseID))
        students = []
        for student in studentIDs:
            info = self.execute("SELECT Name, Surname, PersonID, Email FROM %s.members WHERE PersonID = '%s'" % (organization, student[0]))[0]
            students.append(info)

        return students

    def get_lecturer_courses(self, organization, username):
        self.execute("USE %s" % organization)
        command = "SELECT courses.Name, courses.CODE FROM lecturers JOIN courses ON lecturers.CourseID = courses.CourseID JOIN members ON members.PersonID = lecturers.LecturerID WHERE members.Username = '%s';" % (username)
        lectureIDs = self.execute(command)
        return lectureIDs

    def get_user_info(self, organization, username):
        return self.execute("SELECT * FROM %s.members WHERE Username='%s'" % (organization, username))[0]

    def execute(self, command):
        a = command.replace(";", ";--").split("--")
        try:
            for i in a:
                if len(i)>5:
                    self.cursor.execute(i)

            rtn = self.cursor.fetchall()
            self.__commit()
            return rtn
        except:
            return None
        # try:
        #     self.cursor.execute(command)
        #     print command
        #     rtn = self.cursor.fetchone()
        #     self.__commit()
        #     return rtn
        #
        # except:
        #     return None

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

    # todo: fatihgulmez; use JOIN query.
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
            check = self.execute("Insert into %s.members(PersonID, Role, Name, Surname, Username, Password, Email, Department) values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(organization, student_number, role, name, surname, username, pas.hashPassword(password), mail, department))
            if check is not None:
                auth.append((name + " " + surname, mail, password, username))
            reg.append(student_number)
        threading.Thread(target=sentMail, args=(auth, lecturer)).start()
        print auth, lecturer
        self.register_student(reg, course, organization)
        return "Done"

    # todo: fatihgulmez; use JOIN query.
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

    # todo: fatihgulmez; use JOIN query.
    def delete_student_course(self, organization, course, studentID):
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE Code = '%s'" % (organization, course))[0][0]
        command = "DELETE FROM %s.registrations WHERE StudentID = %d AND CourseID = %d" % (organization, int(studentID), int(courseID))
        self.execute(command)
        return None

    def add_answer(self, organization, exam_name, username, answers):
        try:
            exam_id = self.execute("SELECT examID FROM %s.exams WHERE Name = '%s'" %(organization, exam_name))[0][0]
            student_id = self.execute("SELECT personID FROM %s.members WHERE username = '%s'" %(organization, username))[0][0]
            command = "INSERT INTO %s.answers(examID, studentID, answers) VALUES ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE answers = '%s'" %(organization, exam_id, student_id, answers, answers)
            return self.execute(command)
        except Exception:
            return "Error occurred."



class Password:
    def __init__(self):
        pass

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


class DBTable:
    def __init__(self, name, columns, primary_key=None, foreign_keys_tuple=None, uniques=None, database=None):
        """
        Creates SQL query codes for creating a table in MySQL DBs.
        Also Can directly create table with Database param.
        :param name: string, name of table in database.
        :param columns: list of tuples; ( ColumnName, ColumnType, ColumnsSettings )
        :param primary_key: string, primary key column name
        :param foreign_keys_tuple: list of tuples, each foreign key as a tuple; ( ColumnName, referenceTable, referenceColumn)
        :param uniques: list of tuples, a tuple for a unique constraint; ( *ColumnNames )
        :param database: Database object, optional, for use direct table creation.
        """

        self.command = "CREATE TABLE %s ( " %name
        self.columns = columns
        self.name = name
        self.pk = primary_key
        self.foreign_keys = foreign_keys_tuple
        self.uniques = uniques
        self.db = database

        for column in columns:
            self.command += "%s %s %s, " % column

        self.command = self.command[:len(self.command)-2] + " "

        if primary_key is not None:
            self.PrimaryKey(primary_key)

        if foreign_keys_tuple is not None:
            for foreign in foreign_keys_tuple:
                col = foreign[0]
                ref = foreign[1], foreign[2]
                self.ForeignKey(col, ref)

        if uniques is not None:
            for unique in uniques:
                self.Unique(unique)

        self.command = self.command + ");\n" if self.command != "" else ""
        self.db.execute(self.command)

    def PrimaryKey(self, column):
        self.command += ", primary key (%s)" % column

    def ForeignKey(self, column, referenceTuple):
        self.command += ", foreign key (%s) references %s(%s)" % (column, referenceTuple[0], referenceTuple[1])

    def Unique(self, columnTuple):
        if type(columnTuple) == tuple:
            self.command += ", Unique %s" % str(columnTuple).replace("\'", "")
        else:
            self.command += ", Unique (%s)" % columnTuple

    def insert(self, key_values):
        """
        :param key_values: list of tuples, each tuple contains column nmae-value pairs, *( ColumnName, ColumnValue )
        :return: None
        """
        pass

    def get_command(self):
        return self.command


class Question:
    def __init__(self, tip, subject, text, answer, inputs, outputs, value, tags):
        self.tip = tip
        self.subject = subject
        self.text = text
        self.tags = tags
        self.answer = answer
        self.inputs = inputs
        self.outputs = outputs
        self.value = value
        self.get ={"type": self.tip,
                "subject": self.subject,
                "text": self.text,
                "answer": self.answer,
                "inputs": self.inputs,
                "outputs": self.outputs,
                "value": self.value,
                "tags" : self.tags
                }

    def getString(self):
        return json.dumps(self.get)

    def save(self, db, course_code, organization, exam_code):
        org = organization.replace(" ", "_").lower()
        course_code = course_code.lower().replace(" ", "_")
        command = "USE %s;" %org
        command += "INSERT INTO questions (info, examID) select \'%s\' , ExamID from (select exams.ExamID, exams.CourseID, courses.CODE from exams join courses where exams.CourseID = courses.CourseID and exams.ExamID = %d) as T where T.CODE = \'%s\';" %(self.getString(), exam_code, course_code)
        return db.execute(command)

    def save_command(self, course_code, exam_name):
        course_code = course_code.lower().replace(" ", "_")
        command = "INSERT INTO questions (info, ExamID) select \'%s\' , ExamID from (select exams.ExamID, exams.CourseID, courses.CODE from exams join courses where exams.CourseID = courses.CourseID and exams.Name = \'%s\') as T where T.CODE = \'%s\';" %(self.getString(), exam_name, course_code)
        return command

    def load(self, db, id, organization):
        org = organization.replace(" ", "_").lower()
        # command = "USE %s;" %org
        command = "SELECT * FROM %s.questions WHERE questionID = %d;" % (org, int(id))

        data = db.execute(command)[0]
        return json.dumps({
            "question id": data[0],
            "exam id": data[1],
            "info": json.loads(data[2])
        })

    def load_command(self, db, id, organization):
        pass


class Exam:
    def __init__(self, Name, CourseCode, Time, duration, organization):
        self.org = organization.replace(" ", "_").lower()
        self.name = Name
        self.course = CourseCode.replace(" ", "_").lower()
        self.time = Time
        self.duration = duration
        self.questions = list()

    def addQuestion(self, tip, subject, text, answer, inputs, outputs, value, tags):
        self.questions.append(Question(tip, subject, text, answer, inputs, outputs, value, tags))

    def addQuestionObject(self, questionObj):
        self.questions.append(questionObj)

    def save(self, db):
        """
            use istanbul_sehir_university;
            insert into exams(Name,Time,CourseID) select 'bioinformatics mt 1', '2018-02-15 10:30:00', ID from courses where courses.CODE = 'eecs_468';
        """

        command = "USE %s;" % self.org
        command += " insert into exams(Name,Time,Duration,CourseID) select \'%s\', \'%s\', %d, CourseID from courses where courses.CODE = \'%s\';" % (self.name, self.time, int(self.duration), self.course)

        for question in self.questions:
            command += question.save_command(self.course, self.name)

        db.execute(command)
        return db.execute("SELECT ExamID FROM exams WHERE Name = '%s'" % self.name)[0][0]

    def get(self, db):
        command = "select time, duration from %s.exams where name = '%s'" %(self.org, self.name)
        saved = db.execute(command)
        command = "SELECT info FROM %s.questions join %s.exams where %s.exams.Name = '%s' and %s.questions.examID = %s.exams.examID;" % (self.org, self.org, self.org, self.name, self.org, self.org)
        raw_questions = db.execute(command)
        questions = {}
        i = 0
        for question in raw_questions:
            i = i+1
            questions[i] = question[0]
        for question in self.questions:
            i = i+1
            questions[i] = question.get
        return{
            "Name": self.name,
            "Course": self.course,
            "Time": saved[0][0],
            "Duration": saved[0][1],
            "Questions": questions
        }

    def getString(self, db):
        return json.dumps(self.get(db))


if __name__ == "__main__":
    a = DBTable("example",
                [
                    ("col1", "Varchar(255)", "not null"),
                    ("col2", "int", "auto_increment")
                ],
                primary_key="col2",
                foreign_keys_tuple=[("col2", "courses", "ID")],
                uniques=[("col1", "col2")])
