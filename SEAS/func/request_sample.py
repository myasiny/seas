# -*- coding:UTF-8 -*-

from database_api import *

import threading

# Since DEBUG mode is on, you can use this tokens.
# superuser_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1ZmNiNmY5OC0xYTY2LTQ0ZTQtYWY3ZS01ZWRmZDUwYWUzNTMiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjk3OSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjk3OSwiaWRlbnRpdHkiOlsic3VwZXJ1c2VyIiwic3VwZXJ1c2VyIiwiMjAxOC0wMy0wMSAxNToyMjo1OS40MjQwMDAiXX0.lgvPgmJQ8Ua01oxBBdabaayVdbJhO0W5D3hRBL3Nlbg"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4Y2Y0YzAwYi1iYjQxLTRjY2YtYjY1Yy1lMDYyNmQ3OTY5ZjIiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQxNjc0MCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQxNjc0MCwiaWRlbnRpdHkiOlsiYWRtaW4iLCJhZG1pbiIsIjIwMTgtMDMtMTkgMDI6NDU6NDAuMDg5MDAwIiwiaXN0YW5idWxfc2VoaXJfdW5pdmVyc2l0eSJdfQ.SKZAbZmb1zPqNmjCu746mrnb37oLwzdle85JTIl1lYc"
lecturer_token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0NDIyYmU3MC01NGEwLTQ5NGMtYjQ4MC00MGZiMzIyMDYwNDUiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQxNjc3MywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQxNjc3MywiaWRlbnRpdHkiOlsiYWxpY2FrbWFrIiwibGVjdHVyZXIiLCIyMDE4LTAzLTE5IDAyOjQ2OjEzLjc3MDAwMCIsImlzdGFuYnVsX3NlaGlyX3VuaXZlcnNpdHkiXX0.ix0hSvTZaDfjWIliyxvz2anaUrdPNmMZEBDhtagUJdg"
student_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1MTg1MGFlYS0yMzBiLTQzMWUtOTBmYi00YWFlZmI4OWY4YzgiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQxNjY4MiwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQxNjY4MiwiaWRlbnRpdHkiOlsiZmF0aWhndWxtZXoiLCJzdHVkZW50IiwiMjAxOC0wMy0xOSAwMjo0NDo0Mi42MjEwMDAiLCJpc3RhbmJ1bF9zZWhpcl91bml2ZXJzaXR5Il19.8SwQSb41Hbquq-eLZV5p3bmkbto5KIq3JqaQQQJTnSU"

### Sample usage of API

# print testConnection()

# print addOrganization(superuser_token)
# print addOrganization(superuser_token, organization="istanbul chnical university", URL="http://10.50.81.24:8888")
#
# print addUser(admin_token, "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser(admin_token, "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345","muhamed@std.sehir.edu.tr", "Computer Science" , role="student")
# print addUser(admin_token, "213944444", "Ali Emre", "Oz", "alioz", "12345", "alioz@std.sehir.edu.tr", "Computer Science" ,role="student")
# print addUser(admin_token, "000000000", "Admin", "Admin", "admin", "12345", "admin@admin.com", "admin", role="Admin")
#
# print addUser(admin_token, "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print addUser(admin_token, "215000000", "Ozkan", "Çaglar", "ozkancaglar", "12345","ozkancaglar@std.sehir.edu.tr", "Computer Science", role="student")

# print signIn("fatihgulmez", "123456")
# print signIn("admin", "12345")
# print signIn("superuser", "12345")
# print signIn("alicakmak", "12345")



# print addCourse(admin_token, "Bioinformatics", "eecs 468", ["alicakmak"])
# print getCourse(student_token, "eecs 468")
#
# print registerStudent(lecturer_token, "EECS 468", True, "ornek.csv")

# print getCourseStudents(lecturer_token, "Eecs 468")

# print getUserCourses(lecturer_token, "alicakmak")

# print getUserCourses(student_token, "fatihgulmez")

# print changePassword(student_token, "fatihgulmez", "7P7nDyjq", "12345", False)

# print deleteStudentFromLecture(lecturer_token, "EEcs 468", "213962062")

#### HOW TO CREATE EXAM

# print createExam(lecturer_token,
#                  "EECS 468",
#                  "bioinformatic mt 3",
#                  "2018-03-15 10:30:00",
#                  50
#                  ,
#                  status="draft"
# )

#                   {1:
#                       {"type": "classic",
#                         "subject": "ataturk",
#                         "text": "who is the founder of TR?",
#                         "answer": "Ataturk",
#                         "inputs": [[1,2],[2,3]],
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
#                  ,3:
#                      {"type": "test",
#                       "subject": "math",
#                       "text": "which is an integer? -a)1,2 -b)3/7 -c)5 -d)pi",
#                       "answer": "c",
#                       "inputs": "",
#                       "outputs": "",
#                       "value": 20,
#                       "tags": ["integers", "math"]
#                      }
#                   }


# print addQuestionToExam(lecturer_token, "EECS 468", "aa", {"type": "test",
#                       "subject": "math",
#                       "text": "which is an integer? -a)1,2 -b)3/7 -c)5 -d)pi",
#                       "answer": "c",
#                       "inputs": "",
#                       "outputs": "",
#                       "value": 20,
#                       "tags": ["integers", "math"]
#                      })


## HOW TO GET EXAM
# print getExam(student_token,
#                  "EECS 468",
#                  "aa")

# print sendAnswers(student_token,"EECS 468", 13, "fatihgulmez", "Ataturk")

# print deleteExam(lecturer_token, "bioinformatic_mt_3", "eecs_468")

# print uploadProfilePic(student_token, "fatihgulmez", "picc.png")

# print getProfilePic(student_token, "fatihgulmez")

# print grade_answer(lecturer_token, "eecs 468", 1, "fatihgulmez", 60)

# print getExamsOfLecture(student_token, "eecs 468")

# print edit_question(lecturer_token, "eecs 468",
#                     "bioinformatic_mt_2",
#                     13,
#                     {"type": "classic",
#                     "subject": "ataturk",
#                     "text": "who is the founder of Turkey?",
#                     "answer": "Atatürk",
#                     "inputs": [[111,222],[222,333]],
#                     "outputs": [(3),(5)],
#                     "value": 30,
#                     "tags": ["mustapha","kemal"]})

# print add_time_to_exam(lecturer_token,
#                        "eecs 468",
#                        "bioinformatic_mt_2",
#                        10)

# print change_status_of_exam(lecturer_token,
#                             "eecs 468",
#                             "bioinformatic_mt_2",
#                             "active")

# print resetPassword("fatihgulmez")

# print resetPassword("fatihgulmez", temp_pass="HIk6hx0k", new_pass="123456")

# print signIn("fatihgulmez", "123456")