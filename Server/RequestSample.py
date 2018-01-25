# -*- coding:UTF-8 -*-

from requests import put, get, post, delete
from DatabaseAPI import *

### Sample usage of API

# print testConnection("http://10.50.81.24:8888")

# print addOrganization("http://10.50.81.24:8888", "Istanbul Sehir University")
# print addOrganization("http://10.50.81.24:8888", "Istanbul Technical University")

# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345","muhamed@std.sehir.edu.tr", "Computer Science" , role="student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "213944444", "Ali Emre", "Oz", "alioz", "12345", "alioz@std.sehir.edu.tr", "Computer Science" ,role="student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "000000000", "Admin", "Admin", "admin", "12345", "admin@admin.com", "admin", role="Admin")

# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "000000000", "Joe", "Doe", "joedoe", "12345", "joe@doe.com", "Computer Science", role="Student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "215000000", "Özkan", "Çağlar", "ozkancaglar", "12345","ozkancaglar@std.sehir.edu.tr", "Computer Science", role="student")

# print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "fatihgulmez", "12345")
# print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "aliozz", "12345")

# print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "alicakmak", "12345")
# print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "admin", "12345")

# print signOut("http://10.50.81.24:8888", "Istanbul Sehir University", "admin")

# print addCourse("http://10.50.81.24:8888", "istanbul sehir university", "Introduction to Programming", "ENGR 101", "alicakmak")
# print getCourse("http://10.50.81.24:8888", "istanbul sehir university", "ENGR 101")

# print registerStudent("http://10.50.81.24:8888", "Istanbul Sehir University", "EECS 468", True, "ornek.csv")

# print getCourseStudents("http://10.50.81.24:8888", "Istanbul Sehir University", "ENGR 101")

# print getLecturerCourses("http://10.50.81.24:8888", "Istanbul Sehir University", "alicakmak")

# print changePassword("http://10.50.81.24:8888", "Istanbul Sehir University", "alicakmak", "12345", "alicakmak@sehir.edu.tr", True)

# print deleteStudentFromLecture("http://10.50.81.24:8888", "Istanbul Sehir University", "ENGR 101", "212980975")

# print createExam("http://10.50.81.24:8888",
#                  "Istanbul Sehir University",
#                  "EECS 468",
#                  "bioinformatic mt 1",
#                  "2018-03-15 10:30:00",
#                  50,
#                  {1:
#                       {"type": "classic",
#                         "subject": "ataturk",
#                         "text": "who is the founder of TR?",
#                         "answer": "Ataturk",
#                         "inputs": [(1,2),(2,3)],
#                         "outputs": [(3),(5)],
#                           "value": 50,
#                           "tags": ["mustafa","kemal"]},
#                  2:
#                      {"type": "truefalse",
#                       "subject": "history",
#                       "text": "ottomans were muslims.",
#                       "answer": "true",
#                       "inputs": "",
#                       "outputs": "",
#                       "value": 50,
#                       "tags": ["ottomans", "muslims"]}
#                   }
#                  )

print getExam("http://10.50.81.24:8888",
                 "Istanbul Sehir University",
                 "EECS 468",
                 "bioinformatic mt 2")