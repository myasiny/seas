from External_Functions.handleTR import handle_tr
from External_Functions.sendEmail import send_mail_first_login
from External_Functions.passwordGenerator import passwordGenerator
from Password import Password
import csv, pickle, threading

class Course:
    def __init__(self, db, organization, code, name = None, lecturers =None):
        self.db = db
        self.execute = db.execute
        self.execute("USE %s;" % organization)
        self.organization = organization
        self.code = code
        self.lecture_id = None
        self.lecturers = None
        self.name = None
        if name is None and lecturers is None:
            self.get_course()
        elif name is not None and lecturers is not None:
            self.add_course(name, lecturers)
        else:
            raise AttributeError("Both name and lecturer should be None or both should have values.")

    def add_course(self, name, lecturer_users):
        self.name = name
        self.execute("INSERT INTO courses (NAME, CODE) VALUES ('%s', '%s');"%(name, self.code))
        self.lecture_id =self.execute("select CourseID from courses where CODE = '%s'" % self.code)[0][0]
        command = ""
        self.lecturers = []
        lecturer_users = pickle.loads(lecturer_users)
        if len(lecturer_users) > 0:
            for lecturer in lecturer_users:
                l = self.execute("SELECT Name, Surname, PersonID, Email, Username FROM members WHERE Username = '%s'" % (lecturer))[0]
                self.lecturers.append(l)
                command += "insert into lecturers (LecturerID, CourseID) VALUES ('%s', '%s');" % (l[2], self.lecture_id)
        self.execute(command)
        return "Course Added!"

    def get_course(self):
        a = self.execute("SELECT * FROM courses WHERE Code = '%s'" % (self.code))[0]
        lecturer_IDs = self.execute("SELECT LecturerID FROM lecturers WHERE CourseID = '%s'"%(a[0]))
        self.lecturers = []
        full_name_lecturers = []
        for id in lecturer_IDs:
            username = self.execute("SELECT Name, Surname, PersonID, Email, Username FROM members WHERE PersonID = '%s'" % (id[0]))[0]
            self.lecturers.append(username)
            full_name_lecturers.append(username[0] + " " + username[1])
        self.lecture_id = a[0]
        self.name = a[1]
        self.get = {
            "ID": a[0],
            "Name": a[1],
            "Code": a[2],
            "Lecturers": full_name_lecturers,
            "Participants": self.get_course_participants()
        }

    def register_student(self, studentIDList):
        for i in studentIDList:
            self.execute("INSERT INTO registrations (StudentID, CourseID) VALUES(%s, %s)" %(i, self.lecture_id))

    def get_course_participants(self):
        studentIDs = self.execute("SELECT StudentID FROM registrations WHERE CourseID = '%s'" %self.lecture_id)
        students = []
        for id in studentIDs:
            info = self.execute("SELECT Name, Surname, PersonID, Email, Username FROM members WHERE PersonID = '%s'" % (id[0]))[0]
            students.append(info)

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
        command = "DELETE FROM registrations WHERE StudentID = %d AND CourseID = %d" % (
        int(studentID), int(self.code))
        return self.execute(command)

    def get_exams_of_lecture(self):
        return self.execute("select * from exams where CourseID = '%s'" % (self.lecture_id))
