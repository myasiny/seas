#-*-coding:utf-8-*-
import sys

from requests import put, get, delete, ConnectionError
import json
import re


def testConnection(URL):
    try:
        return True
    except ConnectionError:
        return False


def addOrganization(URL, Organization, token):
    Organization = Organization.replace(" ", "_").lower()
    url = URL+"/organizations"
    return put(url, data={"data": Organization},
        headers = {"Authorization": "Bearer %s" %token}).json()


def addUser(URL, organization, token,  id, name, surname, username, password, Email, Department ,role="student"):
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


def signIn(URL, organization, username, password):
    url = URL+"/organizations/%s/%s" %(organization.replace(" ", "_").lower(), username)
    return get(url, auth=(username, password)).json()


def signOut(URL, organization, token, username):
    url = URL + "/organizations/%s/%s/out" % (organization.replace(" ", "_").lower(), username)
    return get(url, data={
        "Username": username,
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def addCourse(URL, organization, token, courseName, courseCode, *lecturer_users):
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


def getCourse(URL, organization, token, courseCode):
    # type: (str, str, str) -> str
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/get" % (organization, courseCode)
    return get(url, data={
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def registerStudent(URL, organization, token, courseCode, isList, students, username):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL+"/organizations/%s/%s/register/%s" %(organization, courseCode, isList)
    students = open(students)
    if isList:
        return put(url, files={"liste": students}, data={"username": username},
        headers = {"Authorization": "Bearer %s" %token}).json()
    else:
        pass


def getCourseStudents(URL, organization, token, courseCode):
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/register" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getLecturerCourses(URL, organization, token, username):
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/courses/role=lecturer" % (organization, username)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def changePassword(URL, organization, token, username, password, newpass, isMail=False):
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/edit_password" % (organization, username)
    return put(url, data={
        "Password": password,
        "newPassword": newpass,
        "isMail": isMail
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


def deleteStudentFromLecture(URL, organization, token, courseCode, studentID):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/delete_user" % (organization, courseCode)
    return delete(url, data={"Student": studentID},
        headers = {"Authorization": "Bearer %s" %token}).json()


def createExam(URL, organization, token, courseCode, name, time, duration, questions={}):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/add" % (organization, courseCode)
    question = json.dumps(questions)
    return put(url, data={"name": name, "time": time, "duration": duration, "questions": question},
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExamsOfLecture(URL, organization, token, courseCode):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/" % (organization, courseCode)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


def getExam(URL, organization, token, courseCode, name):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    name = re.sub(r'[^\w\s]', '_', name).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s" % (organization, courseCode, name)
    return get(url, headers = {"Authorization": "Bearer " + token}).json()


def sendAnswers(URL, organization, token, courseCode, examName, username, answers):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    examName = re.sub(r'[^\w\s]', '_', examName).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/answers/%s" % (organization, courseCode, examName, username)
    return put(url, data={"answers" : json.dumps(answers)}, headers={"Authorization": "Bearer " + token}).json()

def deleteExam(URL, organization, token, examName, courseCode):
    organization = organization.replace(" ", "_").lower()
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    examName = re.sub(r'[^\w\s]', '_', examName).replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s/exams/%s/delete" % (organization, courseCode, examName)
    return delete(url,
               headers={"Authorization": "Bearer %s" % token}).json()
