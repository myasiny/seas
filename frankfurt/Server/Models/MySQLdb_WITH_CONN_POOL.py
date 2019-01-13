# -*-coding:utf-8-*-
from DBTable import DBTable
from mysql.connector import pooling, InterfaceError, OperationalError
from Password import Password


class MySQLdb:
    def __init__(self, db_name, user="root", password="Dragos!2017"):
        self.name = db_name
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}
        db_config = {
            "pool_name": "conn",
            "database": db_name,
            "user": user,
            "password": password,
            "host": '35.205.88.46',
            "port": 3306,
            "pool_size": 1}

        self.pool = pooling.MySQLConnectionPool(**db_config)

        self.db = None
        self.cursor = None

    def __enter__(self):
        self.db = self.pool.get_connection()
        self.cursor = self.db.cursor(buffered=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.db.close()
            self.db = None
            self.cursor = None
        except OperationalError:
            pass

    def initialize_organization(self, organization):
        # Create Database for organization
        self.execute(
            "CREATE SCHEMA %s;" % organization
        )

        # Set active database and Enable Event Scheduler
        self.execute(
            "USE %s; "
            "SET GLOBAL event_scheduler = ON;" % organization
        )

        # Role Table
        DBTable("roles", [
            ("Role", "varchar(20)", ""),
            ("roleID", "INT", "AUTO_INCREMENT")],
                uniques=[("Role")],
                primary_key="RoleID",
                database=self)

        # Initialize Roles
        self.execute("Insert into roles(Role) values ('superuser'), ('admin'), ('lecturer'), ('student');")

        # Members Table
        DBTable("members", [
            ("PersonID", "int", "not null"),
            ("Role", "int", "not null"),
            ("Name", "varchar(255)", "not null"),
            ("Surname", "varchar(255)", "not null"),
            ("Username", "varchar(255)", "not null"),
            ("Password", "varchar(255)", "not null"),
            ("Email", "varchar(50)", "not null"),
            ("Department", "varchar(255)", ""),
            ("ProfilePic", "varchar(255)", "")],
                primary_key="PersonID",
                foreign_keys_tuple=[("Role", "roles", "RoleID", "")],
                uniques=[("Name", "Surname", "Username"), ("Username")],
                database=self)

        # Courses Table
        DBTable("courses", [
           ("CourseID", "int", "not null auto_increment"),
           ("Name", "varchar(255)", "not null"),
           ("Code", "varchar(20)", "not null"),
           ("isActive", "boolean", "default true")],
               primary_key="CourseID",
               uniques=[("Name", "Code", "isActive")],
               indexes=[("Code")],
               database=self)

        # Registrations Table
        DBTable("registrations", [
            ("StudentID", "int", "not null"),
            ("CourseID", "int", "not null"),
            ("RegistrationID", "int", "auto_increment")],
                foreign_keys_tuple=[
                    ("StudentID", "members", "PersonID", "on delete cascade"),
                    ("courseID", "courses", "CourseID", "on delete cascade")],
                uniques=[
                    ("StudentID", "CourseID")],
                primary_key="RegistrationID",
                database=self)

        # Lecturers Table
        DBTable("lecturers", [
            ("LecturerID", "int", "not null"),
            ("CourseID", "int", "not null"),
            ("LeCorID", "int", "not null auto_increment")],
                foreign_keys_tuple=[
                    ("LecturerID", "members", "PersonID", "on delete cascade"),
                    ("CourseID", "courses", "CourseID", "on delete cascade")],
                primary_key="LeCorID",
                uniques=[
                    ("LecturerID, CourseID")],
                database=self)

    # Exams Table
        DBTable("exams", [
            ("ExamID", "int", "auto_increment"),
            ("Name", "varchar(255)", "not null"),
            ("CourseID", "int", ""),
            ("Time", "Varchar(50)", "not null"),
            ("Duration", "int", "not null"),
            ("Status", "varchar(20)", "not null Default 'draft'")],
                primary_key="ExamID",
                foreign_keys_tuple=[
                    ("CourseID", "courses", "CourseID", "on delete set null")],
                uniques=[
                    ("Name"),
                    ("Name", "Time")],
                database=self)

        # Questions Table
        DBTable("questions", [
            ("QuestionID", "int", "auto_increment"),
            ("ExamID", "int", ""),
            ("info", "JSON", "")],
                primary_key="QuestionID",
                foreign_keys_tuple=[
                    ("ExamID", "exams", "ExamID", "on delete set  null")],
                database=self)

        # Answers Table
        DBTable("answers", [
            ("answerID", "int", "auto_increment"),
            ("questionID", "int", "not null"),
            ("studentID", "int", "not null"),
            ("answer", "JSON", ""),
            ("grade", "int", "")],
                primary_key="answerID",
                foreign_keys_tuple=[
                    ("questionID", "questions", "questionID", "on delete cascade"),
                   ("studentID", "members", "PersonID", "on delete cascade")],
                uniques=[
                   ("questionID", "studentID")],
                database=self)

        # Temporary Passwords Table
        DBTable("temporary_passwords", [
            ("UserID", "int", ""),
            ("Password", "Varchar(255)", "not null")],
                primary_key="UserID",
                foreign_keys_tuple=[
                   ("UserID", "members", "PersonID", "on delete cascade")],
                database=self)

        return "Done"

    def get_organization(self):
        return self.execute("Select * from istanbul_sehir_university.members")

    def sign_up_user(self, organization, request):
        passwd = Password().hash_password(request.form["Password"])
        username = request.form["Username"]
        role = request.form["Role"].lower()
        command = "Insert into %s.members(PersonID, Role, Name, Surname, Username, Password, Email, Department) " \
                  "values(%s, '%d', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (organization,
                     request.form["ID"],
                     int(self.execute("SELECT RoleID FROM %s.roles WHERE Role = '%s'" % (
                         organization, role))[0][0]),
                     request.form["Name"],
                     request.form["Surname"],
                     username,
                     passwd,
                     request.form["Email"],
                     request.form["Department"]
                     )
        return self.execute(command)

    def if_token_revoked(self, token):
        try:
            result = self.execute("select token from main.revoked_tokens where token = '%s'" % token)
            return len(result) > 0
        except InterfaceError:
            return False
        except  TypeError:
            return False

    def revoke_token(self, token):
        return self.execute("INSERT INTO main.revoked_tokens (token) VALUES ('%s');" % token)

    def log_activity(self, username, ip, endpoint, desc=None):
        if desc is None:
            self.execute(
                "INSERT INTO last_activities(Username, IP, Api_Endpoint) VALUES ('%s', '%s', '%s');"
                % (username, ip, endpoint))
        else:
            self.execute(
                "INSERT INTO last_activities(Username, IP, Api_Endpoint, Description) VALUES ('%s', '%s', '%s', '%s');"
                % (username, ip, endpoint, desc))

    def execute(self, command):
        try:
            self.cursor.execute(command)
        except InterfaceError:
            self.cursor.execute(command, multi=True)

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
