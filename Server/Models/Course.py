from External_Functions.handleTR import handle_tr
from External_Functions.sendEmail import send_mail_first_login
from External_Functions.passwordGenerator import passwordGenerator
from Password import Password
from mysql.connector import IntegrityError
import csv
import pickle
import threading


class Course:
    def __init__(self, db, organization, code):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s;" % organization)
        self.organization = organization
        self.code = code

    def add_course(self, name, lecturer_users):
        sql = "INSERT INTO courses (NAME, CODE) VALUES ('%s', '%s');" % (name, self.code)
        command = ""
        lecturer_users = pickle.loads(lecturer_users)
        if len(lecturer_users) > 0:
            for lecturer in lecturer_users:
                command += "((select PersonID from members where Username = '%s')," \
                           "(select CourseID from courses where CODE = '%s'))," % (lecturer, self.code)
        c = "insert into lecturers (LecturerID, CourseID) VALUES %s;" % command[:-1]
        self.execute(sql)
        self.execute(c)
        return "Course Added!"

    def get_course(self):
        course = self.execute("SELECT c.CourseID, c.Name, c.Code FROM courses c Where c.Code = '%s'" % self.code)[0]
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
                    AND l.CourseID = '%s'
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
                    AND a.roleID = m.Role);""" % (course[0], course[0])
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

    def register_student(self, student_id_list):
        lecture_id = self.execute("Select c.courseID as id from courses c where c.Code = '%s';" % self.code)[0][0]
        ids = ""
        for i in student_id_list:
            ids += "(%s, %s)," % (i, lecture_id)
        ids = ids[0:-1] + ";"
        self.execute(" INSERT IGNORE INTO registrations (StudentID, CourseID) VALUES " + ids)

    def get_course_participants(self):
        students = self.execute("Select m.Name, m.Surname, m.PersonID, m.Email, m.Username "
                                "from members m, registrations r where m.PersonID = r.StudentID and "
                                "r.CourseID =(Select CourseID from courses where courses.Code = '%s')" % self.code)
        return students

    def register_student_csv(self, csv_data_file, lecturer):
        csv_reader = csv.reader(csv_data_file)
        data = list(csv_reader)
        auth = []
        reg = []
        pas = Password()
        first = True
        for i in data:
            if first:
                first = False
                continue
            name = handle_tr(i[0]).title()
            surname = handle_tr(i[1]).title()
            student_number = str(int(float(i[2])))
            mail = i[3]
            role = 4
            username = name.split()[0].lower() + surname.lower()
            password = passwordGenerator(8)
            try:
                self.execute("INSERT INTO members(PersonID, Role, Name, Surname, Username, Password, Email) "
                                     "values(%s, '%s', '%s', '%s', '%s', '%s', '%s');"
                                     % (student_number, role, name, surname, username, pas.hash_password(password), mail))
                auth.append((name + " " + surname, mail, password, username))
            except IntegrityError:
                pass
            reg.append(student_number)
        threading.Thread(target=send_mail_first_login, args=(auth, lecturer)).start()
        self.register_student(reg)
        return "Done"

    def delete_student_course(self, student_id):
        command = "DELETE FROM registrations where StudentID = %d and " \
                  "CourseID = (Select courseID from courses where Code = '%s')" % (int(student_id), self.code)
        return self.execute(command)

    def get_exams_of_lecture(self, student=False):
        # if student:
        #     return self.execute("select * from exams where CourseID = (select CourseID from courses where Code = '%s') "
        #                         "and not Status = 'draft'" % self.code)

        return self.execute("select * from exams where CourseID = (select CourseID from courses where Code = '%s')"
                            % self.code)
