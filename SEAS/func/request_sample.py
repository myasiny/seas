# -*- coding:UTF-8 -*-

from database_api import *

def get_token(role):
    if role == "student":
        username, password = "alioz", "1"
    elif role == "lecturer":
        username, password = "alicakmak", "12345"
    else: #Admin
        username, password = "admin", "12345"

    auth = signIn(username, password)
    print auth
    return auth[-1]

# student_token = get_token("student")
# print student_token
lecturer_token = get_token("lecturer")
# print lecturer_token
# admin_token = get_token("admin")
# print admin_token

### Sample usage of API

# print testConnection()

# print addOrganization(superuser_token)
# print addOrganization(admin_token, organization="istanbul technical university")
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhOGVjMDExZS1mNjk0LTRlMTgtYTBiYy0zY2YxYmY0NDI5YTYiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMzY0MzQ1MiwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMzY0MzQ1MiwiaWRlbnRpdHkiOnsidXNlcm5hbWUiOiJmYXRpaGd1bG1leiIsIm9yZ2FuaXphdGlvbiI6ImlzdGFuYnVsX3NlaGlyX3VuaXZlcnNpdHkiLCJyb2xlIjoic3R1ZGVudCIsImlkIjoyMTM5NjIwNjIsInRpbWUiOiIyMDE4LTA0LTEzIDIxOjE3OjMyLjExMzA1NCJ9fQ.v2FNUOoNQ8UneNsT4iRY_u1pSDzybmeoK8ZQO00Pw-s
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5ZGIxMWU2My03Y2Y0LTRhZTAtYWZmMi0wNWU5NjQ4ZGM0ZjciLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyMzY0MzQ4NSwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyMzY0MzQ4NSwiaWRlbnRpdHkiOnsidXNlcm5hbWUiOiJmYXRpaGd1bG1leiIsIm9yZ2FuaXphdGlvbiI6ImlzdGFuYnVsX3NlaGlyX3VuaXZlcnNpdHkiLCJyb2xlIjoic3R1ZGVudCIsImlkIjoyMTM5NjIwNjIsInRpbWUiOiIyMDE4LTA0LTEzIDIxOjE4OjA1LjEwNDgyNSJ9fQ.15WVY0UQCQMd-OCsi6S6onP_-Yt36ZTA1klu3qCFrkg
# print addUser(admin_token, "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser(admin_token, "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345","muhamed@std.sehir.edu.tr", "Computer Science" , role="student")
# print addUser(admin_token, "213944444", "Ali Emre", "Oz", "alioz", "12345", "alioz@std.sehir.edu.tr", "Computer Science" ,role="student")
# print addUser(admin_token, "000000000", "Admin", "Admin", "admin", "12345", "admin@admin.com", "admin", role="Admin")
#
# print addUser(admin_token, "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print addUser(admin_token, "215000000", "Ozkan", "Çaglar", "ozkancaglar", "12345","ozkancaglar@std.sehir.edu.tr", "Computer Science", role="student")

# print addCourse(admin_token, "Data Analytics", "data 102", ["alicakmak"])
# print getCourse(lecturer_token, "data_101")
#
# print registerStudent(lecturer_token, "data 101", True, "ornek.csv", "alicakmak")

# print registerStudent(lecturer_token, "data 101", False, [213860387, 212011111, 212980975, 213860387], "alicakmak")

# print getCourseStudents(lecturer_token, "data 101")

# print getUserCourses(lecturer_token, "alicakmak")

# print getUserCourses(student_token, "fatihgulmez")
#
# print changePassword(student_token, "fatihgulmez", "a", "123456", False)

# print deleteStudentFromLecture(lecturer_token, "Data 101", "210111111")

#### HOW TO CREATE EXAM

# print createExam(lecturer_token,
#                  "data 101",
#                  "FCG TEST",
#                  "2018-04-26 22:30:00",
#                  5,
#                  status="draft"
# )
#
# print add_time_to_exam(lecturer_token,
#                        "data 101",
#                        "fcg test",
#                        10)

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

#
# print addQuestionToExam(lecturer_token, "data 101", "fcg test", {"type": "test",
#                       "subject": "math",
#                       "text": "which is an integer? -a)1,2 -b)3/7 -c)5 -d)pi",
#                       "answer": "c",
#                       "inputs": "",
#                       "outputs": "",
#                       "value": 20,
#                       "tags": ["integers", "math"]
#                      })


## HOW TO GET EXAM
# print getExam(lecturer_token,
#                  "data 101",
#                  "fcg test")

# print sendAnswers(student_token,"EECS 468", 53, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 54, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 55, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 56, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 57, "alioz", "A")

# print deleteExam(lecturer_token, "fcg test", "data_101")

# print uploadProfilePic(student_token, "fatihgulmez", "picc.png")

# print getProfilePic(lecturer_token, "alicakmak")

# print grade_answer(lecturer_token,"eecs 468", 53, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 54, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 55, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 56, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 57, "alioz", 2)

# print getExamsOfLecture(lecturer_token, "data 101")

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



# print change_status_of_exam(lecturer_token,
#                             "data 101",
#                             "data_mt_1",
#                             "draft")

# print resetPassword("alioz")

# print resetPassword("alioz", temp_pass="zD7ric2V", new_pass="1")

print getGradesOfExam(lecturer_token, "eecs 468", "test 2")


print signOut(lecturer_token, "alicakmak")
# print signOut(student_token, "alioz")
# print signOut(admin_token, "admin")