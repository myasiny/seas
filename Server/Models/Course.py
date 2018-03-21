from External_Functions.handleTR import handle_tr
from External_Functions.sendEmail import send_mail_first_login
from External_Functions.passwordGenerator import passwordGenerator
from Password import Password
import csv, pickle, threading

class Course:
    def __init__(self, db, organization, code):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s;" % organization)
        self.organization = organization
        self.code = code

    def add_course(self, name, lecturer_users): # 3 queries
        self.execute("INSERT INTO courses (NAME, CODE) VALUES ('%s', '%s');"%(name, self.code))
        lecture_id = self.execute(" select CourseID from courses where CODE = '%s';" % self.code)[0][0]
        command = ""
        lecturer_users = pickle.loads(lecturer_users)
        if len(lecturer_users) > 0:
            for lecturer in lecturer_users:
                command += "((select PersonID from members where Username = '%s'), '%s')," % (lecturer, lecture_id)
        self.execute("insert into lecturers (LecturerID, CourseID) VALUES " + command[:-1] + ";")
        return "Course Added!"

    def get_course(self):
        course = self.execute(self.select_org + "SELECT c.CourseID, c.Name, c.Code FROM courses c Where c.Code = '%s'" % (self.code))[0]
        people = self.execute(
        """(SELECT 
                CONCAT(m.Name, ' ', m.Surname) AS 'Full Name',
                m.PersonID,
                m.Email,
                m.Username,
                a.Role
            FROM
                members m
            JOIN
                (lecturers l, roles a) ON m.PersonID = l.LecturerID
                AND l.CourseID = '3'
                AND a.roleID = m.Role) 
                UNION ALL 
            (SELECT 
                CONCAT(m.Name, ' ', m.Surname) AS 'Full Name',
                m.PersonID,
                m.Email,
                m.Username,
                a.Role
            FROM
                members m
            JOIN
                (registrations r, roles a) ON m.PersonID = r.StudentID
                AND r.CourseID = '%s'
                AND a.roleID = m.Role);""" %course[0]
        )

        lecturer_name = []
        student_info = []
        for person in people:
            if person[-1] == "lecturer":
                lecturer_name.append(person[0])
            else:
                student_info.append(person)
        return {
            "ID": course[0],
            "Name": course[1],
            "Code": course[2],
            "Lecturers": lecturer_name,
            "Participants": student_info
        }

    def register_student(self, studentIDList):
        lecture_id = self.execute("Select c.courseID as id from courses c where c.Code = '%s';" %self.code)[0][0]
        ids = ""
        for i in studentIDList:
            ids += "(%s, %s)," %(i, lecture_id)
        ids = ids[0:-1] + ";"
        self.execute(" INSERT INTO registrations (StudentID, CourseID) VALUES " + ids)

    def get_course_participants(self):
        students = self.execute("Select m.Name, m.Surname, m.PersonID, m.Email, m.Username from members m join (registrations r, courses c) on m.PersonID = r.StudentID and c.code = '%s';" %self.code)
        return students

    def register_student_csv(self, csvDataFile, lecturer):
        csvReader = csv.reader(csvDataFile)
        column_names = next(csvReader, None)
        data = list(csvReader)
        auth = []
        reg = []
        pas = Password()
        for i in data:
            name = handle_tr(i[0]).title()
            surname = handle_tr(i[1]).title()
            student_number = str(int(float(i[2])))
            mail = i[3]
            role = 4
            username = name.split()[0].lower() + surname.lower()
            password = passwordGenerator(8)
            check = self.execute("Insert into members(PersonID, Role, Name, Surname, Username, Password, Email) values(%s, '%s', '%s', '%s', '%s', '%s', '%s');" % (student_number, role, name, surname, username, pas.hash_password(password), mail))
            if check is not None:
                auth.append((name + " " + surname, mail, password, username))
            reg.append(student_number)
        threading.Thread(target=send_mail_first_login, args=(auth, lecturer)).start()
        self.register_student(reg)
        return "Done"

    def delete_student_course(self, studentID):
        command = "DELETE FROM registrations where StudentID = %d and CourseID = (Select courseID from courses where Code = '%s')" % (
        int(studentID), self.code)
        return self.execute(command)

    def get_exams_of_lecture(self):
        return self.execute("select * from exams where CourseID = (select CourseID from courses where Code = '%s)'" % (self.code))
