#-*-coding:utf-8-*-
import os
from Password import Password

class User:
    """
    todo: Data structure of Users, operations will be moved here!
    """
    def __init__(self, db):
        self.db
        pass

    def get_user_info(self, organization, username):
        """
        :param organization:
        :param username:
        :return: List, [studentID, roleID, name, surname, username, password_hash, email, department, profile_pic_path]
        """
        return self.execute("SELECT * FROM %s.members WHERE Username='%s'" % (organization, username))[0]

    def change_password_or_email(self, organization, username, oldPassword, newVal, email=False):
        pas = Password()
        user = self.get_user_info(organization, username)
        password = user[5]
        if pas.verify_password_hash(oldPassword, password):
            if email:
                self.execute(
                    "UPDATE %s.members SET Email='%s' WHERE Username = '%s'" % (organization, newVal, username))
                return "Mail Changed"
            else:
                password = pas.hash_password(newVal)
                self.execute("UPDATE %s.members SET Password='%s' WHERE Username = '%s'" % (organization, password, username))
                return "Password Changed"
        else:
            return "Not Authorized"

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


class Lecturer(User):
    def __init__(self):
        pass

    def get_lecturer_courses(self, organization, username):
        self.execute("USE %s" % organization)
        command = "SELECT courses.Name, courses.CODE FROM lecturers JOIN courses ON lecturers.CourseID = courses.CourseID JOIN members ON members.PersonID = lecturers.LecturerID WHERE members.Username = '%s';" % (username)
        lectureIDs = self.execute(command)
        return lectureIDs

    def grade_answer(self, organization, username, student_name, question_id, grade):
        studentID = self.get_user_info(organization, student_name)[0]
        c = "INSERT INTO %s.answers(questionID, studentID, grade) VALUES ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE grade=VALUES(grade)" % (organization, str(question_id), studentID, str(grade))
        return self.execute(c)


class Student(User):
    def __init__(self, db):
        pass

    def get_student_courses(self, organization, username):
        self.execute("USE %s" % organization)
        command = "SELECT courses.Name, courses.CODE FROM registrations JOIN courses ON registrations.CourseID = courses.CourseID JOIN members ON members.PersonID = registrations.studentID WHERE members.Username = '%s';" % (
            username)
        lectureIDs = self.execute(command)
        return lectureIDs

    def add_answer(self, organization, question_id, username, answer):
        try:
            student_id = self.execute("SELECT personID FROM %s.members WHERE username = '%s'" %(organization, username))[0][0]
            command = "INSERT INTO %s.answers(questionID, studentID, answer) VALUES ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE answer = '%s'" %(organization, question_id, student_id, answer, answer)
            return self.execute(command)
        except Exception:
            return "Error occurred."
