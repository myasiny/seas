# -*- coding:UTF-8 -*-

from GUI.func.database_api import *
import sys
sys.path.append("..")

address = "10.50.81.24"

# Since DEBUG mode is on, you can use this tokens.
superuser_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1ZmNiNmY5OC0xYTY2LTQ0ZTQtYWY3ZS01ZWRmZDUwYWUzNTMiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjk3OSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjk3OSwiaWRlbnRpdHkiOlsic3VwZXJ1c2VyIiwic3VwZXJ1c2VyIiwiMjAxOC0wMy0wMSAxNToyMjo1OS40MjQwMDAiXX0.lgvPgmJQ8Ua01oxBBdabaayVdbJhO0W5D3hRBL3Nlbg"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4Y2Y5NTVjYS00YmFlLTQyOTYtOWM3Mi00MjczNjk1YjBhMjEiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjk3OCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjk3OCwiaWRlbnRpdHkiOlsiYWRtaW4iLCJhZG1pbiIsIjIwMTgtMDMtMDEgMTU6MjI6NTguNjcxMDAwIl19.Althj6VLLQEAsEukPG20eF1ga7MHyqe9QmUt1gmAhg8"
lecturer_token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIwMTMyYmM0NC1iYzJhLTQxOTAtOGIxYy0xZmE1YTFjMDljMTciLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjUyNSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjUyNSwiaWRlbnRpdHkiOlsiYWxpY2FrbWFrIiwibGVjdHVyZXIiLCIyMDE4LTAzLTAxIDE1OjE1OjI1LjgyMDAwMCJdfQ.RNwBvbZ4iYXzf3rwTIXiIQy-Nx0uzz2RztJSoVwNkc8"
student_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzNjQzNzk2ZC1lN2U2LTQ3NjgtYjVkZS0zZWMxYTQyNDYzOWYiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUxOTkwNjkxMSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUxOTkwNjkxMSwiaWRlbnRpdHkiOlsiZmF0aWhndWxtZXoiLCJzdHVkZW50IiwiMjAxOC0wMy0wMSAxNToyMTo1MS4wNjQwMDAiXX0.Xfd0FoSERqGI-86L2UVmmMwfRDBU1uy9HLMcp5jfThU"

### Sample usage of API

# print testConnection()

# print addOrganization(superuser_token)
# print addOrganization(superuser_token)

# print addUser(admin_token, "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser(admin_token, "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345","muhamed@std.sehir.edu.tr", "Computer Science" , role="student")
# print addUser(admin_token, "213944444", "Ali Emre", "Oz", "alioz", "12345", "alioz@std.sehir.edu.tr", "Computer Science" ,role="student")
# print addUser(admin_token, "000000000", "Admin", "Admin", "admin", "12345", "admin@admin.com", "admin", role="Admin")

# print addUser(admin_token, "000000000", "Joe", "Doe", "joedoe", "12345", "joe@doe.com", "Computer Science", role="Student")
# print addUser(admin_token, "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print addUser(admin_token, "215000000", "Özkan", "Çağlar", "ozkancaglar", "12345","ozkancaglar@std.sehir.edu.tr", "Computer Science", role="student")

# print signIn("fatihgulmez", "12345")
# print signIn("admin", "12345")
# print signIn("superuser", "12345")
# print signIn("alicakmak", "12345")

# print signOut("admin")

# print addCourse(admin_token, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MjFhMmFkZi03NWMwLTQ1ZWItYTg1Yy00ZmNjNzM4MmFmNGUiLCJleHAiOjE1MTk3NjE1NTYsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTE5NzYwNjU2LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTE5NzYwNjU2LCJpZGVudGl0eSI6WyJmYXRpaGd1bG1leiIsInN0dWRlbnQiLCIyMDE4LTAyLTI3IDIyOjQ0OjE2Ljk4MDAwMCJdfQ.UCa5uiyoS-HUWt0ti_TMB61LEHDeXTmCeNjxfkgoyLA", "Bioinformatics", "EECS 468", "alicakmak")
# print getCourse(student_token, "ENGR 101")

# print registerStudent(lecturer_token, "EECS 468", True, "ornek.csv")

# print getCourseStudents(lecturer_token, "ENGR 101")

# print getLecturerCourses(lecturer_token, "alicakmak")

print getLecturerCourses(student_token, "fatihgulmez")


# print changePassword(lecturer_token, "alicakmak", "12345", "alicakmak@sehir.edu.tr", True)

# print deleteStudentFromLecture(lecturer_token, "ENGR 101", "212980975")

#### HOW TO CREATE EXAM

# print createExam(lecturer_token,
#                  "EECS 468",
#                  "bioinformatic mt 2",
#                  "2018-03-15 10:30:00",
#                  50
#                  ,{1:
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
#                   },
#                  status="published"
# )


### HOW TO GET EXAM
# print getExam(student_token,
#                  "EECS 468",
#                  "bioinformatic mt 2")

# print sendAnswers(student_token,"EECS 468", 1, "fatihgulmez", "Atatürk")

# print deleteExam(lecturer_token, "bioinformatic_mt_2", "eecs_468")

# print uploadProfilePic(student_token, "fatihgulmez", "picc.jpg")

# print getProfilePic(student_token, "fatihgulmez")

# print grade_answer(lecturer_token, "eecs 468", 1, "fatihgulmez", 60)

# print getExamsOfLecture(student_token, "eecs 468")