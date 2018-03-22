# -*- coding:UTF-8 -*-

from database_api import *

import threading

# Since DEBUG mode is on, you can use this tokens.
# superuser_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1ZmNiNmY5OC0xYTY2LTQ0ZTQtYWY3ZS01ZWRmZDUwYWUzNTMiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjk3OSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjk3OSwiaWRlbnRpdHkiOlsic3VwZXJ1c2VyIiwic3VwZXJ1c2VyIiwiMjAxOC0wMy0wMSAxNToyMjo1OS40MjQwMDAiXX0.lgvPgmJQ8Ua01oxBBdabaayVdbJhO0W5D3hRBL3Nlbg"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhY2EwNDkxYy0wNWE4LTQ1MzMtODA1NC05MzIyMTNlMGM0OTIiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQ2MTAzOCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQ2MTAzOCwiaWRlbnRpdHkiOnsidXNlcm5hbWUiOiJhZG1pbiIsIm9yZ2FuaXphdGlvbiI6ImlzdGFuYnVsX3NlaGlyX3VuaXZlcnNpdHkiLCJyb2xlIjoiYWRtaW4iLCJ0aW1lIjoiMjAxOC0wMy0xOSAxNTowMzo1OC43NjgwMDAifX0.QUVp_RGqrnyUMt_-UY_2qFBk1Wab1-U_7IFwLWxwVDQ"
lecturer_token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmOTliMzA4NC1iMjBiLTQwYjUtYjA0OC00ZmE2MThhNjAxZWIiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQ2MTAwNywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQ2MTAwNywiaWRlbnRpdHkiOnsidXNlcm5hbWUiOiJhbGljYWttYWsiLCJvcmdhbml6YXRpb24iOiJpc3RhbmJ1bF9zZWhpcl91bml2ZXJzaXR5Iiwicm9sZSI6ImxlY3R1cmVyIiwidGltZSI6IjIwMTgtMDMtMTkgMTU6MDM6MjcuOTAyMDAwIn19.gbTw0JFNUAIXUK4cmWGEYatsCWux9kJEXcX8jaR7n-s"
student_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1MmM2NzQyMi01MWVkLTQyOWUtYWE1Yy0zZDA2YzM3NWRmNmQiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMTQ2MTAzNywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMTQ2MTAzNywiaWRlbnRpdHkiOnsidXNlcm5hbWUiOiJmYXRpaGd1bG1leiIsIm9yZ2FuaXphdGlvbiI6ImlzdGFuYnVsX3NlaGlyX3VuaXZlcnNpdHkiLCJyb2xlIjoic3R1ZGVudCIsInRpbWUiOiIyMDE4LTAzLTE5IDE1OjAzOjU3LjIzODAwMCJ9fQ.TXsck-9VUD25Jx5zgY3svfoJZX1HMl_89_LBhc4g-N0"

### Sample usage of API

# print testConnection()

# print addOrganization(superuser_token)
print addOrganization(admin_token, organization="istanbul technical university")
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

# print addCourse(admin_token, "Physics", "phys 101", ["alicakmak"])
# print getCourse(lecturer_token, "phys_101")
#
# print registerStudent(lecturer_token, "EECS 468", True, "ornek.csv", "alicakmak")
# print registerStudent(lecturer_token, "phys 101", False, [213962062, 212011111, 212980975, 213860387], "alicakmak")


# print getCourseStudents(lecturer_token, "Eecs 468")

# print getUserCourses(lecturer_token, "alicakmak")

# print getUserCourses(student_token, "fatihgulmez")

# print changePassword(student_token, "fatihgulmez", "7P7nDyjq", "12345", False)

# print deleteStudentFromLecture(lecturer_token, "EEcs 468", "214578451")

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
#                  "as")

# print sendAnswers(student_token,"EECS 468", 13, "fatihgulmez", "Ataturk")

# print deleteExam(lecturer_token, "as", "eecs_468")

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

# print reset_password("fatihgulmez")

# print reset_password("fatihgulmez", temp_pass="HIk6hx0k", new_pass="123456")

# print signIn("fatihgulmez", "123456")