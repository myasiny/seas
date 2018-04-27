#-*-coding:utf-8-*-
import mysql.connector
from DBTable import DBTable
from mysql.connector import pooling, InterfaceError, PoolError, OperationalError

class MySQLdb:
    def __init__(self, dbName, user="root", password="Dragos!2017"):
        self.name = dbName
        self.allowed_extensions = set(['png', 'jpg', 'jpeg'])
        dbconfig = {
            "database": dbName,
            "user": user,
            "password": password,
            "host": '35.205.88.46',
            "port":3306
        }

        self.pool = pooling.MySQLConnectionPool(pool_name="conn",
                                       pool_size=1,pool_reset_session=True, buffered=True,
                                       **dbconfig)

    def __enter__(self):
        self.get_connection()
        # try:
        #     self.get_connection()
        # except PoolError:
        #     self.close_connection()
        #     self.get_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        # try:
        #     self.close_connection()
        # except OperationalError:
        #     print "already disconnected"

    def get_connection(self):
        self.db = self.pool.get_connection()
        self.cursor = self.db.cursor(buffered=True)

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

        self.execute("Insert into roles(Role) values ('superuser'); "
                     "Insert into roles(Role) values ('admin'); "
                     "Insert into roles(Role) values ('lecturer');"
                     "Insert into roles(Role) values ('student');")

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
                                  ("Department", "varchar(255)", ""),
                                  ("ProfilePic", "varchar(255)", "")
                              ],
                              primary_key="PersonID",
                              foreign_keys_tuple=[("Role", "roles", "RoleID", "")],
                              uniques=[("Name", "Surname", "Username"), ("Username")],
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
                               indexes=[("Code")],
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
                                 ("Time", "Varchar(50)", "not null"),
                                 ("Duration", "int", "not null"),
                                 ("Status", "varchar(20)", "not null Default 'draft'")
                             ],
                             primary_key="ExamID",
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
        return "Done"

    def get_organization(self):
        return self.execute("Select * from istanbul_sehir_university.members")
        pass

    def if_token_revoked(self, token):
        # try:
        result = self.execute("select token from main.revoked_tokens where token = '%s'" %(token))
        print result
        return len(result) > 0
        # except InterfaceError:
        #     print "1"
        #     return False
        # except  TypeError:
        #     print "2"
        #     return False

    def revoke_token(self, token):
        return self.execute("INSERT INTO main.revoked_tokens (token) VALUES ('%s');" %token)

    def execute(self, command):
        try:
            self.cursor.fetchall()
        except:
            pass

        try:
            self.cursor.execute(command)
        except InterfaceError:
            self.cursor.execute(command, multi=True)
            print "Interface error 1"


        if command.lower().startswith("select") or command.lower().startswith("(select"):
            rtn = self.cursor.fetchall()
            self.__commit()
            return rtn
        try:
            self.__commit()
        except InterfaceError:
            for result in self.db.cmd_query_iter(command):
                print "cmd_query_iter: ", result
                self.__commit()
        return None
        # try:
        #     rtn = self.cursor.fetchall()
        # except InterfaceError:
        #     print "Interface error 2"
        #     rtn = None
        # self.__commit()
        # return rtn
    def __commit(self):
        return self.db.commit()
