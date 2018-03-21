#-*-coding:utf-8-*-
from flaskext.mysql import MySQL
from DBTable import DBTable
from Password import Password
from External_Functions.passwordGenerator import passwordGenerator
from External_Functions.sendEmail import send_mail_first_login
import csv, threading, os

class MySQLdb:
    def __init__(self, dbName, app, user="tester", password="wivern@seas"):
        self.mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = dbName
        app.config['MYSQL_DATABASE_HOST'] = '159.65.124.42'
        app.config['MYSQL_DATABASE_PORT'] = 8000
        self.name = dbName
        self.allowed_extensions = set(['png', 'jpg', 'jpeg'])
        self.mysql.init_app(app)

        self.db = self.mysql.connect()
        self.cursor = self.db.cursor()

    def initialize_organization(self, organization):
        a = self.execute(
            "CREATE SCHEMA %s;" %organization
        )
        self.execute(
            "USE %s; "
            "SET GLOBAL event_scheduler = ON;" %organization
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
                                  ("Role", "int", "not null Default 4"),
                                  ("Name", "varchar(255)", "not null"),
                                  ("Surname", "varchar(255)", "not null"),
                                  ("Username", "varchar(255)", "not null"),
                                  ("Password", "varchar(255)", "not null"),
                                  ("Email", "varchar(50)", "not null"),
                                  ("Department", "varchar(255)", ""),
                                  ("ProfilePic", "varchar(255)", "")
                              ],
                              primary_key="PersonID",
                              foreign_keys_tuple=[("Role", "roles", "RoleID", "ON DELETE SET NULL")],
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
                                 ("StudentID", "members", "PersonID", "on delete cascade"),
                                 ("courseID", "courses", "CourseID", "on delete cascade")
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
                                     ("LecturerID", "members", "PersonID", "on delete cascade"),
                                     ("CourseID", "courses", "CourseID", "on delete cascade")
                                 ],
                                 primary_key="LeCorID",
                                 uniques=
                                 [
                                     ("LecturerID, CourseID")
                                 ],
                              database=self)

        # command_seq.append(lecturersTable.get_command())

        examsTable = DBTable("exams",
                             [
                                 ("ExamID", "int", "auto_increment"),
                                 ("Name", "varchar(255)", "not null"),
                                 ("CourseID", "int", ""),
                                 ("Time", "timestamp", ""),
                                 ("Duration", "int", "not null"),
                                 ("Status", "varchar(20)", "not null Default 'draft'")
                             ],
                             primary_key="ExamId",
                             foreign_keys_tuple=
                             [
                                 ("CourseID", "courses", "CourseID", "on delete set null")
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
                                 foreign_keys_tuple=
                                 [
                                     ("ExamID", "exams", "ExamID", "on delete set  null")
                                 ],
                              database=self)

        answersTable = DBTable("answers",
                               [
                                   ("answerID", "int", "auto_increment"),
                                   ("questionID", "int", "not null"),
                                   ("studentID", "int", "not null"),
                                   ("answer", "JSON", ""),
                                   ("grade", "int", "")
                               ],
                               primary_key="answerID",
                               foreign_keys_tuple=[
                                   ("questionID", "questions", "questionID", "on delete cascade"),
                                   ("studentID", "members", "PersonID", "on delete cascade")
                               ],
                               uniques=[
                                   ("questionID", "studentID")
                               ],
                               database=self)

        # command_seq.append(questionsTable.get_command())

        temporary_passwordsTable = DBTable("temporary_passwords",
                                           [
                                               ("UserID", "int", ""),
                                               ("Password", "Varchar(255)", "not null")
                                           ],
                                           primary_key="UserID",
                                           foreign_keys_tuple=[
                                               ("UserID", "members", "PersonID", "on delete cascade")
                                           ],
                                           database=self)

        self.execute("Insert into roles(Role) values ('superuser'); "
                     "Insert into roles(Role) values ('admin'); "
                     "Insert into roles(Role) values ('lecturer');"
                     "Insert into roles(Role) values ('student');")

        return a

    def get_organization(self):
        pass

    def if_token_revoked(self, token):
        result = self.execute("select token from main.revoked_tokens where token = '%s'" %(token))
        return len(result) > 0

    def revoke_token(self, token):
        return self.execute("INSERT INTO main.revoked_tokens (token) VALUES ('%s');" %token)

    def execute(self, command):
        self.cursor.execute(command)
        try:
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
