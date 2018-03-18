#-*-coding:utf-8-*-
from flaskext.mysql import MySQL
from DBTable import DBTable
from Password import Password
from External_Functions.passwordGenerator import passwordGenerator
from External_Functions.sendEmail import sentMail
import csv, threading, os

class MySQLdb:
    def __init__(self, dbName, app, user="tester", password="wivern@seas"):
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = dbName
        app.config['MYSQL_DATABASE_HOST'] = '159.65.124.42'
        app.config['MYSQL_DATABASE_PORT'] = 8000
        self.name = dbName
        self.allowed_extensions = set(['png', 'jpg', 'jpeg'])
        mysql.init_app(app)

        self.db = mysql.connect()
        self.cursor = self.db.cursor()

    def initialize_organization(self, organization):
        a = self.execute(
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
                                  ("Department", "varchar(255)", "not null"),
                                  ("ProfilePic", "varchar(255)", "")
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
                                   ("questionID", "int", "not null"),
                                   ("studentID", "int", "not null"),
                                   ("answer", "JSON", ""),
                                   ("grade", "int", "")
                               ],
                               primary_key="answerID",
                               foreign_keys_tuple=[
                                   ("questionID", "questions", "questionID"),
                                   ("studentID", "members", "PersonID")
                               ],
                               uniques=[
                                   ("questionID", "studentID")
                               ],
                               database=self)

        # command_seq.append(questionsTable.get_command())

        revoked_token_table = DBTable("revoked_tokens",
                                      [
                                          ("token", "varchar(255)", "")
                                      ],
                                      primary_key="token",
                                      database=self
                                      )

        self.execute("Insert into roles(Role) values ('superuser'); "
                     "Insert into roles(Role) values ('admin'); "
                     "Insert into roles(Role) values ('lecturer');"
                     "Insert into roles(Role) values ('student');")

        return a

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

    def get_course(self, org, code):
        a = self.execute("SELECT * FROM %s.courses WHERE Code = '%s'" % (org,code))[0]
        lecturer_IDs = self.execute("SELECT LecturerID FROM %s.lecturers WHERE CourseID = '%s'"%(org, a[0]))
        lecturers = []
        for id in lecturer_IDs:
            lid = self.execute("SELECT Name, Surname FROM %s.members WHERE PersonID = '%s'" % (org, id[0]))[0]
            lecturers.append(lid[0] + " " + lid[1])
        rtn = {
            "ID": a[0],
            "Name": a[1],
            "Code": a[2],
            "Lecturers": lecturers,
            "Participants": self.get_course_participants(a[2], org)
        }
        return rtn

    def register_student(self, studentIDList, courseCode, organization):
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE CODE = '%s'" % (organization, courseCode))[0][0]
        for i in studentIDList:
            self.execute("INSERT INTO %s.registrations (StudentID, CourseID) VALUES(%s, %s)" %(organization, i, courseID))
        pass

    def get_course_participants(self, code, organization):
        c = "SELECT CourseID FROM %s.courses WHERE CODE = '%s'" %(organization, code)
        print c
        courseID = self.execute(c)[0][0]
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

    def get_student_courses(self, organization, username):
        self.execute("USE %s" % organization)
        command = "SELECT courses.Name, courses.CODE FROM registrations JOIN courses ON registrations.CourseID = courses.CourseID JOIN members ON members.PersonID = registrations.studentID WHERE members.Username = '%s';" % (
            username)
        lectureIDs = self.execute(command)
        return lectureIDs

    def get_user_info(self, organization, username):
        """
        :param organization:
        :param username:
        :return: List, [studentID, roleID, name, surname, username, password_hash, email, department, profile_pic_path]
        """
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
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE Code = '%s'" % (organization, course))[0][0]
        command = "DELETE FROM %s.registrations WHERE StudentID = %d AND CourseID = %d" % (organization, int(studentID), int(courseID))
        self.execute(command)
        return None

    def add_answer(self, organization, question_id, username, answer):
        try:
            student_id = self.execute("SELECT personID FROM %s.members WHERE username = '%s'" %(organization, username))[0][0]
            command = "INSERT INTO %s.answers(questionID, studentID, answer) VALUES ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE answer = '%s'" %(organization, question_id, student_id, answer, answer)
            return self.execute(command)
        except Exception:
            return "Error occurred."

    def allowed_file(self, filename):  # to check if file type is appropriate.
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload_profile_pic(self, organization, username, pic, content, path):
        if pic and self.allowed_file(pic.filename):
            userID = str(self.get_user_info(organization, username)[0])
            extension = "." + pic.filename.rsplit('.', 1)[1].lower()
            path = path + "media/%s/profiles/" % organization + userID + extension
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, "wb") as f:
                f.write(content)
            self.execute("update %s.members set ProfilePic = '%s' where PersonID = '%s';" %(organization, path, userID))
            return "Done"
        return "Not allowed extension."

    def get_profile_picture(self, organization, username):
        path = self.execute("select ProfilePic from %s.members where Username = '%s'" %(organization, username))[0][0]
        return path

    def grade_answer(self, organization, username, student_name, question_id, grade):
        studentID = self.get_user_info(organization, student_name)[0]
        c = "INSERT INTO %s.answers(questionID, studentID, grade) VALUES ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE grade=VALUES(grade)" % (organization, str(question_id), studentID, str(grade))
        return self.execute(c)

    def get_exams_of_lecture(self, organization, course):
        course_id = self.execute("select CourseID from %s.courses where Code = '%s'" % (organization, course))[0][0]
        return self.execute("select * from %s.exams where CourseID = '%s'" %(organization, course_id))

    def if_token_revoked(self, token):
        result = self.execute("select token from main.revoked_tokens where token = '%s'" %(token))
        return len(result) > 0

    def revoke_token(self, token):
        return self.execute("INSERT INTO main.revoked_tokens (token) VALUES ('%s');" %token)