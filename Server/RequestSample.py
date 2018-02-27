# -*- coding:UTF-8 -*-

from requests import put, get, post, delete
from DatabaseAPI import *
import sys
sys.path.append("..")
from Functionality.excelToCsv import xls2csv

address = "10.50.81.24"

student_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MjFhMmFkZi03NWMwLTQ1ZWItYTg1Yy00ZmNjNzM4MmFmNGUiLCJleHAiOjE1MTk3NjE1NTYsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTE5NzYwNjU2LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTE5NzYwNjU2LCJpZGVudGl0eSI6WyJmYXRpaGd1bG1leiIsInN0dWRlbnQiLCIyMDE4LTAyLTI3IDIyOjQ0OjE2Ljk4MDAwMCJdfQ.UCa5uiyoS-HUWt0ti_TMB61LEHDeXTmCeNjxfkgoyLA"
lecturer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0YWZkOTJjNi04NzU1LTQ0YWEtYTgwZC02OWE5OGVmZDE5MmEiLCJleHAiOjE1MTk3NjI1NDQsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTE5NzYxNjQ0LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTE5NzYxNjQ0LCJpZGVudGl0eSI6WyJhbGljYWttYWsiLCJsZWN0dXJlciIsIjIwMTgtMDItMjcgMjM6MDA6NDQuMDM4MDAwIl19.OP_CQEGHbciDXju6-4UOeZpnpMIu8jrE-aIBci--N2Y"

### Sample usage of API

# print testConnection("http://" + address +":8888")

# print addOrganization("http://" + address +":8888", "Istanbul Sehir University")
# print addOrganization("http://" + address +":8888", "Istanbul Technical University")

# print addUser("http://" + address +":8888", "Istanbul Sehir University", "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser("http://" + address +":8888", "Istanbul Sehir University", "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345","muhamed@std.sehir.edu.tr", "Computer Science" , role="student")
# print addUser("http://" + address +":8888", "Istanbul Sehir University", "213944444", "Ali Emre", "Oz", "alioz", "12345", "alioz@std.sehir.edu.tr", "Computer Science" ,role="student")
# print addUser("http://" + address +":8888", "Istanbul Sehir University", "000000000", "Admin", "Admin", "admin", "12345", "admin@admin.com", "admin", role="Admin")

# print addUser("http://" + address +":8888", "Istanbul Sehir University", "000000000", "Joe", "Doe", "joedoe", "12345", "joe@doe.com", "Computer Science", role="Student")
# print addUser("http://" + address +":8888", "Istanbul Sehir University", "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print addUser("http://" + address +":8888", "Istanbul Sehir University", "215000000", "Özkan", "Çağlar", "ozkancaglar", "12345","ozkancaglar@std.sehir.edu.tr", "Computer Science", role="student")

# print signIn("http://" + address +":8888", "Istanbul Sehir University", "fatihgulmez", "12345")

# print addUser("http://" + address +":8888", "Istanbul Sehir University", "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print signIn("http://" + address +":8888", "Istanbul Sehir University", "fatihgulmez", "12345")

# print signIn("http://" + address +":8888", "Istanbul Sehir University", "alioz", "123")

print signIn("http://" + address +":8888", "Istanbul Sehir University", "alicakmak", "12345")
# print signIn("http://" + address +":8888", "Istanbul Sehir University", "admin", "12345")

# print signOut("http://" + address +":8888", "Istanbul Sehir University", "admin")

# print addCourse("http://" + address +":8888", "istanbul sehir university", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MjFhMmFkZi03NWMwLTQ1ZWItYTg1Yy00ZmNjNzM4MmFmNGUiLCJleHAiOjE1MTk3NjE1NTYsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTE5NzYwNjU2LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTE5NzYwNjU2LCJpZGVudGl0eSI6WyJmYXRpaGd1bG1leiIsInN0dWRlbnQiLCIyMDE4LTAyLTI3IDIyOjQ0OjE2Ljk4MDAwMCJdfQ.UCa5uiyoS-HUWt0ti_TMB61LEHDeXTmCeNjxfkgoyLA", "Bioinformatics", "EECS 468", "alicakmak")
# print getCourse("http://" + address +":8888", "istanbul sehir university", "ENGR 101")

# print registerStudent("http://" + address +":8888", "Istanbul Sehir University", "EECS 468", True, "ornek.csv")

# print getCourseStudents("http://" + address +":8888", "Istanbul Sehir University", "ENGR 101")

# print getLecturerCourses("http://" + address +":8888", "Istanbul Sehir University", "alicakmak")

# print changePassword("http://" + address +":8888", "Istanbul Sehir University", "alicakmak", "12345", "alicakmak@sehir.edu.tr", True)

# print deleteStudentFromLecture("http://" + address +":8888", "Istanbul Sehir University", "ENGR 101", "212980975")

#### HOW TO CREATE EXAM

# print createExam("http://" + address +":8888",
#                  "Istanbul Sehir University",
#                  "EECS 468",
#                  "bioinformatic mt 2",
#                  "2018-03-15 10:30:00",
#                  50
                 # ,{1:
                 #      {"type": "classic",
                 #        "subject": "ataturk",
                 #        "text": "who is the founder of TR?",
                 #        "answer": "Ataturk",
                 #        "inputs": [[1,2],[2,3]],
                 #        "outputs": [(3),(5)],
                 #          "value": 50,
                 #          "tags": ["mustafa","kemal"]},
                 # 2:
                 #     {"type": "truefalse",
                 #      "subject": "history",
                 #      "text": "ottomans were muslims.",
                 #      "answer": "true",
                 #      "inputs": "",
                 #      "outputs": "",
                 #      "value": 50,
                 #      "tags": ["ottomans", "muslims"]}
                 #  }
# )


### HOW TO GET EXAM
# print getExam("http://" + address +":8888",
#                  "Istanbul Sehir University",
#                  "EECS 468",
#                  "bioinformatic mt 2")


# print addUser("http://" + address +":8888", "Istanbul Technical University", "213962062", "Fatih", "gulmez", "fatihgulmez", "12345","fatihgulmez@std.sehir.edu.tr", "Computer Science", role="student")
# print addUser("http://" + address +":8888", "Istanbul Technical University", "1", "Ali", "Cakmak", "alicakmak", "12345", "joe@doe.com", "Computer Science", role="Lecturer")
# print signIn("http://" + address +":8888", "Istanbul Technical University", "fatihgulmez", "12345")
# print addCourse("http://" + address +":8888", "Istanbul Technical University", "Introduction to Programming", "ENGR 101", "alicakmak")

# print registerStudent("http://" + address +":8888", "Istanbul Technical University", "ENGR 101", True, "fakelist.csv", "alicakmak")

# print getCourse("http://" + address +":8888", "Istanbul Technical University", "ENGR 101")
# print getCourseStudents("http://" + address +":8888", "Istanbul Technical University", "ENGR 101")
# print getLecturerCourses("http://" + address +":8888", "Istanbul Technical University", "alicakmak")

# print createExam("http://" + address +":8888",
#                  "Istanbul Technical University",
#                  "engr 101",
#                  "bioinformatic mt 2",
#                  "2018-03-15 10:30:00",
#                  50,
#                  {1:
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
#                   }
#                  )


### HOW TO GET EXAM
# print getExam("http://" + address +":8888",
#                  "Istanbul Technical University",
#                  "EECS 468",
#                  "bioinformatic mt 2")

