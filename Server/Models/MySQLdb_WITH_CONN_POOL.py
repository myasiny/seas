#-*-coding:utf-8-*-
import mysql.connector
from DBTable import DBTable
from mysql.connector import pooling, InterfaceError

class MySQLdb:
    def __init__(self, dbName, user="tester", password="wivern@seas"):
        self.name = dbName
        self.allowed_extensions = set(['png', 'jpg', 'jpeg'])
        dbconfig = {
            "database": dbName,
            "user": user,
            "password": password,
            "host": '159.65.124.42',
            "port":8000
        }

        self.pool = pooling.MySQLConnectionPool(pool_name="conn",
                                       pool_size=2,pool_reset_session=True,
                                       **dbconfig)

    def __enter__(self):
        self.get_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def get_connection(self):
        self.db = self.pool.get_connection()
        self.cursor = self.db.cursor(buffered=True)

    def initialize_organization(self, organization):
        self.get_connection()
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
                                 ("Time", "timestamp", ""),
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
        result = self.execute("select token from main.revoked_tokens where token = '%s'" %(token))
        return len(result) > 0

    def revoke_token(self, token):
        return self.execute("INSERT INTO main.revoked_tokens (token) VALUES ('%s');" %token)

    def execute(self, command):
        try:
            self.cursor.execute(command)
        except InterfaceError:
            self.cursor.execute(command, multi=True)


        if command.lower().startswith("select") or command.lower().startswith("(select"):
            rtn = self.cursor.fetchall()
            self.__commit()
            return rtn
        self.__commit()
        return None

    def __commit(self):
        return self.db.commit()
    def close_connection(self):
        self.db.close()

