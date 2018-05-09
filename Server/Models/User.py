# -*-coding:utf-8-*-
import os
import threading
from Password import Password
from External_Functions.passwordGenerator import passwordGenerator
from External_Functions.sendEmail import send_mail_password_reset
from mysql.connector import IntegrityError, InterfaceError


class User:
    def __init__(self, db, organization, username):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s" % organization)
        self.username = username
        self.organization = organization
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}
        self.pass_word = Password()

        self.user_id = None
        self.role = None
        self.name = None
        self.surname = None
        self.hashed_pass = None
        self.email = None
        self.department = None
        self.profile_pic_path = None
        self.role_name = None

        self.get = self.get_user_info()

    def get_user_info(self):
        """
        :return: List, [studentID, roleID, name, surname, username, password_hash, email, department, profile_pic_path]
        """
        try:
            self.user_id, self.role, self.name, self.surname, self.username, self.hashed_pass, self.email, self.department, self.profile_pic_path = self.execute("SELECT * FROM members WHERE Username='%s'" % self.username)[0]

            self.role_name = self.execute("SELECT Role FROM roles WHERE roleID = %s" % self.role)[0][0]
            return [self.username, self.name, self.surname, self.user_id, self.role_name, self.email, self.department]
        except InterfaceError:
            return "No such a person!"

    def change_password_or_email(self, old_password, new_val, email=False):
        if self.pass_word.verify_password_hash(old_password, self.hashed_pass):
            if email:
                self.execute(
                    "UPDATE members SET Email='%s' WHERE Username = '%s'" % (new_val, self.username))
                return "Mail Changed"
            else:
                print new_val
                password = self.pass_word.hash_password(new_val)
                print password
                self.execute("UPDATE members SET Password='%s' WHERE Username = '%s'" % (password, self.username))
                return "Password Changed"
        else:
            return "Not Authorized"

    def allowed_file(self, filename):  # to check if file type is appropriate.
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload_profile_pic(self, pic):
        if pic and self.allowed_file(pic.filename):
            extension = "." + pic.filename.rsplit('.', 1)[1].lower()
            base_path = "uploads/%s/profile_pictures/" % self.organization
            path = base_path + str(self.user_id) + extension
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            with open(path, "wb") as f:
                data = None
                while data != "":
                    data = pic.read()
                    f.write(data)
            self.execute("update members set ProfilePic = '%s' where PersonID = '%s';" % (path, self.user_id))
            return "Done"
        return "Not allowed extension."

    def get_profile_picture(self,):
        return self.profile_pic_path

    def verify_password(self, password):
        return self.pass_word.verify_password_hash(password, self.hashed_pass)

    def reset_password(self):
        password = passwordGenerator(8)
        try:
            password_ = self.pass_word.hash_password(password)
            self.execute("INSERT INTO temporary_passwords (UserID, Password)"
                         "VALUES (%d, '%s');" % (int(self.user_id), password_))
            self.execute("CREATE EVENT user_%d ON SCHEDULE AT date_add(now(), INTERVAL 30 MINUTE) "
                         "DO DELETE FROM temporary_passwords WHERE UserID = %d;"
                         % (int(self.user_id), int(self.user_id)))
            auth = ["%s %s" % (self.name, self.surname), self.email, password, self.username]
            threading.Thread(target=send_mail_password_reset, args=(auth,)).start()
            return "Check your mail address for credentials."
        except IntegrityError:
            return "Your account has been reset already."

    def check_and_change_password(self, temp_pass, new_pass):
        password = self.execute("SELECT Password FROM temporary_passwords WHERE UserID = %d;"
                                % (int(self.user_id)))[0][0]
        if self.pass_word.verify_password_hash(temp_pass, password):
            self.execute("DELETE FROM temporary_passwords WHERE UserID = %d;" % (int(self.user_id)))
            new_pass = self.pass_word.hash_password(new_pass)
            return self.execute("UPDATE members SET members.Password = '%s' WHERE PersonID = %d;"
                                % (new_pass, int(self.user_id)))
        return "Wrong Temporary Password!"

    def get_last_activity(self, endpoint):
        if endpoint == "last_login":
            rtn = self.execute("SELECT Api_Endpoint, Time, IP FROM istanbul_sehir_university.last_activities "
                               "where username = '%s' and Api_Endpoint = 'sign_in' order by Time DESC limit 5;"
                               % self.username)
        else:
            rtn = self.execute("SELECT Api_Endpoint, Time, IP FROM istanbul_sehir_university.last_activities "
                               "where username = '%s' order by Time DESC limit 5;" % self.username)
        return rtn


class Lecturer(User):
    def __init__(self, db, organization, username):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s" % organization)
        self.username = username
        self.organization = organization
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}
        self.pass_word = Password()
        self.get = self.get_user_info()

    def get_lecturer_courses(self):
        return self.execute("SELECT courses.Name, courses.CODE FROM lecturers JOIN courses ON "
                            "lecturers.CourseID = courses.CourseID JOIN members ON "
                            "members.PersonID = lecturers.LecturerID WHERE members.Username = '%s';" % self.username)

    def grade_answer(self, question_id, student, grade):
        return self.execute("INSERT INTO answers(questionID, studentID, grade) VALUES "
                            "('%s', (SELECT PersonID from members where Username = '%s') , '%s') "
                            "ON DUPLICATE KEY UPDATE grade=VALUES(grade)" % (str(question_id), student, str(grade)))


class Student(User):
    def __init__(self, db, organization, username):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s" % organization)
        self.username = username
        self.organization = organization
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}
        self.pass_word = Password()
        self.get = self.get_user_info()

    def get_student_courses(self):
        return self.execute("SELECT courses.Name, courses.CODE FROM registrations JOIN courses ON "
                            "registrations.CourseID = courses.CourseID JOIN members ON "
                            "members.PersonID = registrations.studentID WHERE members.Username = '%s';"
                            % self.username)

    def add_answer(self, question_id, answer):
        try:
            return self.execute("INSERT INTO answers(questionID, studentID, answer) "
                                "select %d, %d, '%s' where "
                                "(Select Status from exams where ExamID = "
                                "(Select ExamId from questions Where QuestionID=%d))='active' "
                                "ON DUPLICATE KEY UPDATE answer = '%s';"
                                % (int(question_id), int(self.user_id), answer, int(question_id), answer))
        except Exception:
            return "Error occurred."
