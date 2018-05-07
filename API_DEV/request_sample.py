# -*- coding:UTF-8 -*-

from database_api import *


def get_token(role):
    if role == "student":
        username, password = "fatihgulmez", "12345"
    elif role == "lecturer":
        username, password = "alicakmak", "1"
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

# print add_course(admin_token, "Data Analytics", "data 102", ["alicakmak"])
# print "get course", getCourse(lecturer_token, "data_101")
#
# print registerStudent(lecturer_token, "data 101", True, "ornek.csv", "alicakmak")

# print "register student", registerStudent(lecturer_token, "data 101", False, [213860387, 212011111, 212980975, 213860387], "alicakmak")

# print "get course students",getCourseStudents(lecturer_token, "data 101")

# print "get user courses",getUserCourses(lecturer_token, "alicakmak")

# print getUserCourses(student_token, "fatihgulmez")
#
# print changePassword(student_token, "fatihgulmez", "123456", "12345", False)

# print "delete student from lecture", deleteStudentFromLecture(lecturer_token, "Data 101", "210111111")

#### HOW TO CREATE EXAM
#
# print "create exam", createExam(lecturer_token,
#                  "data 101",
#                  "FCG TEST",
#                  "2018-12-31 22:30:00",
#                  5,
#                  status="draft"
# )
#
# print "add time to exam", add_time_to_exam(lecturer_token,
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

#
# print "add question to exam", addQuestionToExam(lecturer_token, "data 101", "fcg test", {"type": "test",
#                       "subject": "math",
#                       "text": "which is an integer? -a)1,2 -b)3/7 -c)5 -d)pi",
#                       "answer": "c",
#                       "inputs": "",
#                       "outputs": "",
#                       "value": 20,
#                       "tags": ["integers", "math"]
#                      })


## HOW TO GET EXAM
# print "get exam", getExam(lecturer_token,
#                  "data 101",
#                  "fcg test")

# print getExam(student_token, "data 101", "fcg test 2")
# print sendAnswers(student_token,"Data 101", 97, "fatihgulmez", "A")
# print sendAnswers(student_token,"EECS 468", 54, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 55, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 56, "alioz", "A")
# print sendAnswers(student_token,"EECS 468", 57, "alioz", "A")

# print "delete exam", deleteExam(lecturer_token, "fcg test", "data_101")

# print uploadProfilePic(lecturer_token, "alicakmak", "example_image.png")

# print "profile pic get", getProfilePic(lecturer_token, "alicakmak")

# print grade_answer(lecturer_token,"data 101", 97, "fatihgulmez", 28)
# print grade_answer(lecturer_token,"eecs 468", 54, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 55, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 56, "alioz", 2)
# print grade_answer(lecturer_token,"eecs 468", 57, "alioz", 2)

# print "get exams of lecture", getExamsOfLecture(lecturer_token, "data 101")

# print edit_question(lecturer_token, "data 101",
#                     "fcg test 2",
#                     97,
#                     {"type": "classic",
#                     "subject": "ataturk",
#                     "text": "who is the founder of Turkey?",
#                     "answer": "Atatürk",
#                     "inputs": [[111,222],[222,333]],
#                     "outputs": [(3),(5)],
#                     "value": 30,
#                     "tags": ["mustapha","kemal"]})



# print "change status of exam", change_status_of_exam(lecturer_token,
#                             "data 101",
#                             "fcg test 2",
#                             "graded")

# print resetPassword("alioz")

# print resetPassword("alioz", temp_pass="zD7ric2V", new_pass="1")
# print getGradesOfExam(lecturer_token, "data 101", "test 3")

# print getLastActivities(lecturer_token, "alicakmak", sign_in=True)
# print getLastActivities(lecturer_token, "alicakmak")
# print postExamData(lecturer_token, "eecs 468", "test 1", "alicakmak", "example_data.json")
# print postExamData(lecturer_token, "eecs 468", "test 1", "alicakmak", "example_data")
# print getAnswersOfStudent(lecturer_token, "eecs 468", "test 3", "213962062")
# print extraMaterials(lecturer_token, "eecs 468", "test 1", 149, "example_image.png", "reference", upload=True)

a = 0
while a < 3:
    print sendKeystrokeData(lecturer_token, "eecs 468", "test 1", "1", "asdasd\n")
    print sendKeystrokeData(lecturer_token, "eecs 468", "test 1", "1", "123456\n")
    a += 1

b = getKeystrokeData(lecturer_token, "eecs 468", "test 1", "1")

for line in b:
    print line

print signOut(lecturer_token, "alicakmak")
# print signOut(student_token, "fatihgulmez")
# print signOut(admin_token, "admin")
