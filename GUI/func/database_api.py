# -*-coding:utf-8-*-
import sys
from requests import put, get, delete
from requests.exceptions import ConnectionError, Timeout
import json
import re
import pickle
from config import *

def testConnection(URL=server_address):
    try:
        get(URL, timeout=5)
        return True
    except ConnectionError or Timeout:
        return False


def addOrganization(token, URL=server_address, Organization=current_organization):
    Organization = Organization.replace(" ", "_").lower()
    url = URL+"/organizations"
    return put(url, data={"data": Organization},
        headers = {"Authorization": "Bearer %s" %token}).json()


def addUser(token,  id, name, surname, username, password, Email, Department ,role="student", URL=server_address, organization=current_organization):
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
    url = URL+"/organizations/%s/%s" %(organization.replace(" ", "_").lower(), username)
    return get(url, auth=(username, password)).json()


def signOut(token, username, URL=server_address, organization=current_organization):
    url = URL + "/organizations/%s/%s/out" % (organization.replace(" ", "_").lower(), username)
    return get(url, data={
        "Username": username,
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def addCourse(token, courseName, courseCode, URL=server_address, organization=current_organization, *lecturer_users):
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


def addLecturerToCourse():
    pass


def getCourse(token, courseCode, URL=server_address, organization=current_organization):
    # type: (str, str, str) -> str
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/get" % (organization, courseCode)
    return get(url, data={
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


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
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/register" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getLecturerCourses(token, username, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/courses/role=lecturer" % (organization, username)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def changePassword(token, username, password, newpass, isMail=False, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/edit_password" % (organization, username)
    return put(url, data={
        "Password": password,
        "newPassword": newpass,
        "isMail": isMail
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def deleteStudentFromLecture(token, courseCode, studentID, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/delete_user" % (organization, courseCode)
    return delete(url, data={"Student": studentID},
        headers = {"Authorization": "Bearer %s" %token}).json()


def createExam(token, courseCode, name, time, duration, questions={}, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/add" % (organization, courseCode)
    question = json.dumps(questions)
    return put(url, data={"name": name, "time": time, "duration": duration, "questions": question},
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExamsOfLecture(token, courseCode, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExam(token, courseCode, name, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s" % (organization, courseCode, name)
    return get(url, headers = {"Authorization": "Bearer " + token}).json()


def sendAnswers(token, courseCode, questionID, username, answer, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/answers/%s" % (organization, courseCode, str(questionID), username)
    return put(url, data={"answers" : json.dumps(answer)}, headers={"Authorization": "Bearer " + token}).json()


def deleteExam(token, examName, courseCode, URL=server_address, organization=current_organization):
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
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/pic" %(organization, username)
    with open("sent.jpg", "wb") as f:
        f.write(pickle.loads(get(url, headers={"Authorization": "Bearer " + token}).json()))

    return "Done"


def grade_answer(token, course_code, question_id, student_user, grade, URL=server_address, organization=current_organization):
    organization = organization.replace(" ", "_").lower()
    course_code = re.sub(r'[^\w\s]', '_', course_code).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/answers/%s/grade" % (organization, course_code, str(question_id), student_user)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"grade": grade}).json()
