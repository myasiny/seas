# -*-coding:utf-8-*-
import sys
from requests import put, get, delete
from requests.exceptions import ConnectionError, Timeout
import json
import re
import pickle
from config import *

def testConnection(URL=server_address):
    """
    :param URL: String; server address with port number.
    :return: Boolean; True if connection is done, false otherwise.
    """
    try:
        get(URL, timeout=5)
        return True
    except ConnectionError or Timeout:
        return False


def addOrganization(token, URL=server_address, organization=current_organization):
    """
    :param token: String ;JWT User token, superuser token needed.
    :param URL: String; server address
    :param Organization: String; university name
    :return: [] if organization added, NONE otherwise
    """
    organization = organization.replace(" ", "_").lower()
    url = URL+"/organizations"
    print url, organization
    return put(url, data={"data": organization},
               headers={"Authorization": "Bearer %s" % token}).json()


def addUser(token,  id, name, surname, username, password, Email, Department ,role="student", URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param id: String; user ID (studentID i.e.)
    :param name: String; user's real name
    :param surname: String; user's surname
    :param username: String; username for signing in.
    :param password: String; initial password
    :param Email: String; Email of user
    :param Department: String; Department of user
    :param role: String; Role of user, can be student, lecturer, admin, superuser
    :param URL: String; address of server
    :param organization: String; university name
    :return: [] if successfully added, NONE otherwise or already added.
    """
    url = URL+"/organizations/%s" %organization.replace(" ", "_").lower()
    return put(url,data={
                        "ID": id,
                        "Name": name,
                        "Surname": surname,
                        "Role": role,
                        "Username": username,
                        "Password": password,
                        "Email": Email,
                        "Department": Department
                        },
        headers = {"Authorization": "Bearer %s" %token}).json()


def signIn(username, password, URL=server_address, organization=current_organization):
    """
    :param username: String; username for sign in
    :param password: String; password for sign in
    :param URL: String; address of server
    :param organization: String; university name
    :return: List; [String username, String name, String surname, String user id,
                    String role, String email, String department, String university, String JWT token]
    """
    url = URL+"/organizations/%s/%s" %(organization.replace(" ", "_").lower(), username)
    return get(url, auth=(username, password)).json()


def signOut(token, username, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username
    :param URL: String; Server address
    :param organization: String; university name
    :return: NOT IMPLEMENTED, will Deactivate access token.
    """
    url = URL + "/organizations/%s/%s/out" % (organization.replace(" ", "_").lower(), username)
    return get(url, data={
        "Username": username,
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def addCourse(token, courseName, courseCode, lecturer_users, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param courseName: String; course name
    :param courseCode: String; course code
    :param URL: String; server address
    :param organization: String; university name
    :param lecturer_users: List of Strings; usernames of lecturers of the course
    :return: Course Added if successful.
    """
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    courseName = courseName.replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s" % (organization, courseCode)
    lecturers = ""
    lecturers += lecturer_users[0]
    for lecturer in range(1, len(lecturer_users)):
        lecturers = lecturers + ":" + lecturer_users[lecturer]
    return put(url, data={
        "name": courseName,
        "code": courseCode,
        "lecturers": lecturers},
        headers = {"Authorization": "Bearer %s" %token}
               ).json()


# todo: @fatihgulmez
def addLecturerToCourse():
    pass


def getCourse(token, courseCode, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param courseCode: String; course code
    :param URL: String; server address
    :param organization: String; organization
    :return: JSON; { "Participants": List of lists of all students' data, "Lecturers": List of Strings of Lecturer full Names.
                    "Code": String course code, "ID": Course ID, "Name": Course Name
    """
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/get" % (organization, courseCode)
    return get(url, data={
    },
        headers = {"Authorization": "Bearer %s" %token}).json()

# todo: one student registration
def registerStudent(token, courseCode, isList, students, username, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL+"/organizations/%s/%s/register/%s" %(organization, courseCode, isList)
    students = open(students)
    if isList:
        return put(url, files={"liste": students}, data={"username": username},
        headers = {"Authorization": "Bearer %s" %token}).json()
    else:
        pass


def getCourseStudents(token, courseCode, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param courseCode: String; course code
    :param URL: String; server address
    :param organization: String; university name
    :return: List of Lists of students' name, surname, ID, email.
    """
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/register" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getUserCourses(token, username, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param username: String; username of request
    :param URL: String; server address
    :param organization: String; university name
    :return: List of lists of course name and course code.
    """
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/courses/role=lecturer" % (organization, username)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def changePassword(token, username, password, newpass, isMail=False, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username of request
    :param password: String; old password
    :param newpass: String; new password or Email
    :param isMail: Boolean; True if email change function, False if password change function.
    :param URL: String; server address
    :param organization: String; university name
    :return: String; Mail Changed or Password Change if successful, Not authorized if password is wrong.
    """
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/edit_password" % (organization, username)
    return put(url, data={
        "Password": password,
        "newPassword": newpass,
        "isMail": isMail
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def deleteStudentFromLecture(token, courseCode, studentID, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param courseCode: String; course code
    :param studentID: Integer; student ID
    :param URL: String; server address
    :param organization: String; university name
    :return: NONE
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/delete_user" % (organization, courseCode)
    return delete(url, data={"Student": studentID},
        headers = {"Authorization": "Bearer %s" %token}).json()


def createExam(token, courseCode, name, time, duration, questions={}, status="draft", URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param courseCode: String; course code
    :param name: String; exam name
    :param time: String Timestamp; Start time of exam
    :param duration: Integer; duration of exam in minutes
    :param questions: JSON; {QuestionID:{type: "question type", subject: "question subject", text: "question text",
                    answer:"true answer for this question", inputs:"input values - list of tuples",
                    outputs:"output values, list of tuples", value:"point of question", tags:"list of strings of tags"
    :param status: String; can be draft, completed, graded, ready
    :param URL: String; server address
    :param organization: String; university name
    :return: Integer, ExamID
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/add" % (organization, courseCode)
    question = json.dumps(questions)
    return put(url, data={"name": name, "time": time, "duration": duration, "questions": question, "status": status},
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExamsOfLecture(token, courseCode, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param courseCode: String; course code
    :param URL: String; server address
    :param organization: String; university name
    :return: List of Lists of exams data (ID, name, lecture id, timestamp start time, integer duration (min), status)
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExam(token, courseCode, name, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param courseCode: String; course code
    :param name: String; exam name
    :param URL: String; server address
    :param organization: String; university name
    :return: JSON; Name: String exam name, Course: String course code, Questions: JSON(see create exam questions structure),
                Time: String Timestamp starting time, Duration: Integer exam duration in minutes, ID: Integer exam id
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s" % (organization, courseCode, name)
    return get(url, headers = {"Authorization": "Bearer " + token}).json()


def sendAnswers(token, courseCode, questionID, username, answer, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param courseCode: String; course code
    :param questionID: String; question ID
    :param username: String; username of request
    :param answer: String; user's answer
    :param URL: String; server address
    :param organization: String; university name
    :return: [] if success, NONE otherwise
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/answers/%s" % (organization, courseCode, str(questionID), username)
    return put(url, data={"answers" : json.dumps(answer)}, headers={"Authorization": "Bearer " + token}).json()


def deleteExam(token, examName, courseCode, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param examName: String; exam name to be deleted
    :param courseCode: String; course code of exam
    :param URL: String; server address
    :param organization: String; university name
    :return: [] if successful
    """
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    examName = re.sub(r'[^\w\s]', '_', examName).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/delete" % (organization, courseCode, examName)
    return delete(url,
               headers={"Authorization": "Bearer %s" % token}).json()


def uploadProfilePic(token, username, pic, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/pic" %(organization, username)
    with open(pic, "rb") as f:
        cont = f.read()
    return put(url, headers={"Authorization": "Bearer " + token}, data = {"pic": pickle.dumps(cont)}, files = {"pic": open(pic)}).json()


def getProfilePic(token, username, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username of request
    :param URL: String;  server address
    :param organization: String; university
    :return: Done, saves profile picture to GUI/img/pic_username.png
    """
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/pic" %(organization, username)
    with open("../img/pic_current_user.png", "wb") as f:
        f.write(pickle.loads(get(url, headers={"Authorization": "Bearer " + token}).json()))

    return "Done"


def grade_answer(token, course_code, question_id, student_user, grade, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String, course code
    :param question_id: Integer, question id number
    :param student_user: String; username of answer
    :param grade: Integer; grade of answer
    :param URL: String; Server address
    :param organization: String; university name
    :return: [] if successful.
    """
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/answers/%s/grade" % (organization, course_code, str(question_id), student_user)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"grade": grade}).json()


def edit_question(token, course_code, exam_name, question_id, info, URL=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String, course code
    :param exam_name: String, exam name
    :param question_id: Integer, question id number
    :param info: JSON; question metadata.
    :param URL: String; Server address
    :param organization: String; university name
    :return: [] if successful.
    """
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/%s/edit" % (
    organization, course_code, exam_name, str(question_id))
    return put(url, headers={"Authorization": "Bearer " + token}, data={"data":json.dumps(info)}).json()


def add_time_to_exam(token, course_code, exam_name, additional_time, URL=server_address, organization=current_organization):
    """
    :param token:
    :param course_code:
    :param exam_name:
    :param additional_time:
    :param URL:
    :param organization:
    :return: [] if success
    """
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/more_time" % (organization, course_code, exam_name)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"additional_time": additional_time}).json()


def change_status_of_exam(token, course_code, exam_name, status, URL=server_address, organization=current_organization):
    """
    :param token:
    :param course_code:
    :param exam_name:
    :param status:
    :param URL:
    :param organization:
    :return: [] if success
    """
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/status" % (organization, course_code, exam_name)
    if status not in ["draft", "finished", "published", "graded", "deactivated", "active"]:
        return "Wrong status."
    return put(url, headers={"Authorization": "Bearer " + token}, data={"status": status}).json()



def addQuestionToExam(token, course_code, exam_name, question_info, organization = current_organization, URL = server_address):
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    exam_name = re.sub(r'[^\w\s]', '_', exam_name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/addQuestion" % (organization, course_code, exam_name)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"data": json.dumps(question_info)}).json()