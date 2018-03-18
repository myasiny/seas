#-*-coding:utf-8-*-
import csv, threading
from Password import  Password
from External_Functions import passwordGenerator
from External_Functions.sendEmail import sendMailFirstLogin


class Lecture:
    """
    todo: Data structure of Lectures, operations will be moved here!
    """
    def __init__(self):
        pass

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

    def delete_student_course(self, organization, course, studentID):
        courseID = self.execute("SELECT CourseID FROM %s.courses WHERE Code = '%s'" % (organization, course))[0][0]
        command = "DELETE FROM %s.registrations WHERE StudentID = %d AND CourseID = %d" % (organization, int(studentID), int(courseID))
        self.execute(command)
        return None

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

    def register_student_csv(self, csvDataFile, organization, course, lecturer):
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
        threading.Thread(target=sendMailFirstLogin, args=(auth, lecturer)).start()
        self.register_student(reg, course, organization)
        return "Done"

    def get_exams_of_lecture(self, organization, course):
        course_id = self.execute("select CourseID from %s.courses where Code = '%s'" % (organization, course))[0][0]
        return self.execute("select * from %s.exams where CourseID = '%s'" %(organization, course_id))

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
