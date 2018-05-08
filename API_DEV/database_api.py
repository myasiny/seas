# -*-coding:utf-8-*-
import sys
from requests import put, get, delete
from requests.exceptions import ConnectionError, Timeout
import json
import re
import pickle
from config import *


def __normalize(word):
    word =  re.sub(r'[^\w\s]', '_', word).replace(" ", "_").lower()
    return word


def server_check(func):
    def wrapper(*args, **kwargs):
        try:
            rtn = func(*args, **kwargs)
            if isinstance(rtn, list) and len(rtn) == 1 and rtn[0] == "":
                return []
            return rtn
        except ValueError:
            return "500 - Internal Error"
        except ConnectionError:
            return "404 - Server is not reachable."
    return wrapper


@server_check
def testConnection(base_url=server_address):
    """
    :param base_url: String; server address with port number.
    :return: Boolean; True if connection is done, false otherwise.
    """
    try:
        get(base_url, timeout=5)
        return True
    except ConnectionError or Timeout:
        return False


@server_check
def addOrganization(token, base_url=server_address, organization=current_organization):
    """
    :param token: String ;JWT User token, superuser token needed.
    :param base_url: String; server address
    :param organization: String; university name
    :return: [] if organization added, NONE otherwise
    """
    organization = __normalize(organization)
    url = base_url + "/organizations"
    return put(url, data={"data": organization},
               headers={"Authorization": "Bearer %s" % token}).json()


@server_check
def addUser(token, id_, name, surname, username, password, email, department, role="student",
            base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param id_: String; user ID (studentID i.e.)
    :param name: String; user's real name
    :param surname: String; user's surname
    :param username: String; username for signing in.
    :param password: String; initial password
    :param email: String; Email of user
    :param department: String; Department of user
    :param role: String; Role of user, can be student, lecturer, admin, superuser
    :param base_url: String; address of server
    :param organization: String; university name
    :return: [] if successfully added, NONE otherwise or already added.
    """
    url = base_url + "/organizations/%s" % __normalize(organization)
    return put(url,data={
                        "ID": id_,
                        "Name": name,
                        "Surname": surname,
                        "Role": role,
                        "Username": username,
                        "Password": password,
                        "Email": email,
                        "Department": department
                        },
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def signIn(username, password, base_url=server_address, organization=current_organization):
    """
    :param username: String; username for sign in
    :param password: String; password for sign in
    :param base_url: String; address of server
    :param organization: String; university name
    :return: List; [String username, String name, String surname, String user id,
                    String role, String email, String department, String university, String JWT token]
    """
    url = base_url + "/organizations/%s/%s" % (__normalize(organization), username)
    rtn = get(url, auth=(username, password)).json()
    return rtn


@server_check
def signOut(token, username, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username
    :param base_url: String; Server address
    :param organization: String; university name
    :return: NOT IMPLEMENTED, will Deactivate access token.
    """
    url = base_url + "/organizations/%s/%s/out" % (__normalize(organization), username)
    return put(url, headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def addCourse(token, course_name, course_code, lecturer_users,
              base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param course_name: String; course name
    :param course_code: String; course code
    :param base_url: String; server address
    :param organization: String; university name
    :param lecturer_users: List of Strings; usernames of lecturers of the course
    :return: Course Added if successful.
    """
    course_code = __normalize(course_code)
    course_name = __normalize(course_name)
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s" % (organization, course_code)
    return put(url, data={
        "name": course_name,
        "code": course_code,
        "lecturers": pickle.dumps(lecturer_users)},
        headers = {"Authorization": "Bearer %s" %token}
               ).json()


@server_check
# todo: @fatihgulmez
def addLecturerToCourse():
    pass


@server_check
def getCourse(token, course_code, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String; course code
    :param base_url: String; server address
    :param organization: String; organization
    :return: JSON; { "Participants": List of lists of all students' data, "Lecturers": List of Strings of Lecturer full Names.
                    "Code": String course code, "ID": Course ID, "Name": Course Name
    """
    course_code = __normalize(course_code)
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/get" % (organization, course_code)
    return get(url, data={
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


# todo: one student registration
@server_check
def registerStudent(token, course_code, is_list, students, username,
                    base_url=server_address, organization=current_organization):
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    url = base_url + "/organizations/%s/%s/register/%s" % (organization, course_code, is_list)
    if is_list:
        students = open(students)
        return put(url, files={"liste": students}, data={"username": username},
        headers = {"Authorization": "Bearer %s" %token}).json()
    else:
        return put(url, data={"username": username, "liste": pickle.dumps(students)},
                   headers={"Authorization": "Bearer %s" % token}).json()


@server_check
def getCourseStudents(token, course_code, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param course_code: String; course code
    :param base_url: String; server address
    :param organization: String; university name
    :return: List of Lists of students' name, surname, ID, email.
    """
    course_code =__normalize(course_code)
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/register" % (organization, course_code)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def getUserCourses(token, username, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param username: String; username of request
    :param base_url: String; server address
    :param organization: String; university name
    :return: List of lists of course name and course code.
    """
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/courses/role=lecturer" % (organization, username)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def changePassword(token, username, password, new_password, is_mail=False,
                   base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username of request
    :param password: String; old password
    :param new_password: String; new password or Email
    :param is_mail: Boolean; True if email change function, False if password change function.
    :param base_url: String; server address
    :param organization: String; university name
    :return: String; Mail Changed or Password Change if successful, Not authorized if password is wrong.
    """
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/edit_password" % (organization, username)
    return put(url, data={
        "Password": password,
        "newPassword": new_password,
        "isMail": is_mail
    },
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def deleteStudentFromLecture(token, course_code, student_id,
                             base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String; course code
    :param student_id: Integer; student ID
    :param base_url: String; server address
    :param organization: String; university name
    :return: NONE
    """
    organization =__normalize(organization)
    course_code = __normalize(course_code)
    url = base_url + "/organizations/%s/%s/delete_user" % (organization, course_code)
    return delete(url, data={"Student": student_id},
                  headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def createExam(token, course_code, name, time, duration, status="draft",
               base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param course_code: String; course code
    :param name: String; exam name
    :param time: String Timestamp; Start time of exam
    :param duration: Integer; duration of exam in minutes
    :param status: String; can be draft, completed, graded, ready
    :param base_url: String; server address
    :param organization: String; university name
    :return: Integer, ExamID
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    name = __normalize(name)
    url = base_url + "/organizations/%s/%s/exams/add" % (organization, course_code)
    return put(url, data={"name": name, "time": time, "duration": duration, "status": status},
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def getExamsOfLecture(token, course_code, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT Token
    :param course_code: String; course code
    :param base_url: String; server address
    :param organization: String; university name
    :return: List of Lists of exams data (ID, name, lecture id, timestamp start time, integer duration (min), status)
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    url = base_url + "/organizations/%s/%s/exams/" % (organization, course_code)
    return get(url,
        headers = {"Authorization": "Bearer %s" %token}).json()


@server_check
def getExam(token, course_code, name, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String; course code
    :param name: String; exam name
    :param base_url: String; server address
    :param organization: String; university name
    :return: JSON; Name: String exam name, Course: String course code, Questions: JSON(see create exam questions structure),
                Time: String Timestamp starting time, Duration: Integer exam duration in minutes, ID: Integer exam id
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    name = __normalize(name)
    url = base_url + "/organizations/%s/%s/exams/%s" % (organization, course_code, name)
    return get(url, headers = {"Authorization": "Bearer " + token}).json()


@server_check
def sendAnswers(token, course_code, question_id, username, answer,
                base_url=server_address, organization=current_organization, **kwargs):
    """
    :param token: String; JWT token
    :param course_code: String; course code
    :param question_id: String; question ID
    :param username: String; username of request
    :param answer: String; user's answer
    :param base_url: String; server address
    :param organization: String; university name
    :param kwargs: Dictionary; keys are question_time, compile_number, answer_count
    :return: [] if success, NONE otherwise
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    url = base_url + "/organizations/%s/%s/exams/%s/answers/%s" % (organization, course_code, str(question_id), username)
    return put(url, data={"answers": json.dumps(answer), "question_stats": kwargs}, headers={"Authorization": "Bearer " + token}).json()


@server_check
def deleteExam(token, exam_name, course_code, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param exam_name: String; exam name to be deleted
    :param course_code: String; course code of exam
    :param base_url: String; server address
    :param organization: String; university name
    :return: [] if successful
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    url = base_url + "/organizations/%s/%s/exams/%s/delete" % (organization, course_code, exam_name)
    return delete(url,
               headers={"Authorization": "Bearer %s" % token}).json()


@server_check
def uploadProfilePic(token, username, pic, base_url=server_address, organization=current_organization):
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/pic" % (organization, username)
    return put(url, headers={"Authorization": "Bearer " + token}, files = {"pic": open(pic, "rb")}).json()


@server_check
def getProfilePic(token, username, base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param username: String; username of request
    :param base_url: String;  server address
    :param organization: String; university
    :return: Done, saves profile picture to SEAS/img/pic_username.png
    """
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/pic" % (organization, username)
    try:
        with open("data/img/pic_user_current.png", "wb") as f:
            f.write(pickle.loads(get(url, headers={"Authorization": "Bearer " + token}).json()))
    except TypeError:
        pass

    return "Done"


@server_check
def grade_answer(token, course_code, question_id, student_user, grade,
                 base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String, course code
    :param question_id: Integer, question id number
    :param student_user: String; username of answer
    :param grade: Integer; grade of answer
    :param base_url: String; Server address
    :param organization: String; university name
    :return: [] if successful.
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    url = base_url + "/organizations/%s/%s/exams/%s/answers/%s/grade" % (organization, course_code, str(question_id), student_user)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"grade": grade}).json()


@server_check
def edit_question(token, course_code, exam_name, question_id, info,
                  base_url=server_address, organization=current_organization):
    """
    :param token: String; JWT token
    :param course_code: String, course code
    :param exam_name: String, exam name
    :param question_id: Integer, question id number
    :param info: JSON; question metadata.
    :param base_url: String; Server address
    :param organization: String; university name
    :return: [] if successful.
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    url = base_url + "/organizations/%s/%s/exams/%s/%s/edit" % (
    organization, course_code, exam_name, str(question_id))
    return put(url, headers={"Authorization": "Bearer " + token}, data={"data":json.dumps(info)}).json()


@server_check
def add_time_to_exam(token, course_code, exam_name, additional_time,
                     base_url=server_address, organization=current_organization):
    """
    :param token:
    :param course_code:
    :param exam_name:
    :param additional_time:
    :param base_url:
    :param organization:
    :return: [] if success
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    url = base_url + "/organizations/%s/%s/exams/%s/more_time" % (organization, course_code, exam_name)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"additional_time": additional_time}).json()


@server_check
def change_status_of_exam(token, course_code, exam_name, status,
                          base_url=server_address, organization=current_organization):
    """
    :param token:
    :param course_code:
    :param exam_name:
    :param status:
    :param base_url:
    :param organization:
    :return: [] if success
    """
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    url = base_url + "/organizations/%s/%s/exams/%s/status" % (organization, course_code, exam_name)
    if status not in ["draft", "finished", "published", "graded", "deactivated", "active"]:
        return "Wrong status."
    return put(url, headers={"Authorization": "Bearer " + token}, data={"status": status}).json()


@server_check
def addQuestionToExam(token, course_code, exam_name, question_info,
                      organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    url = base_url + "/organizations/%s/%s/exams/%s/add_question" % (organization, course_code, exam_name)
    return put(url, headers={"Authorization": "Bearer " + token}, data={"data": json.dumps(question_info)}).json()


@server_check
def resetPassword(username, temp_pass=None, new_pass=None,
                  organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    url = base_url + "/organizations/%s/%s/reset_password" % (organization, username)
    if temp_pass is None:
        return get(url).json()
    else:
        return put(url, auth=(temp_pass, new_pass)).json()


@server_check
def getGradesOfExam(token, course_code, exam_name, student_id="ALL",
                    organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    course_code = __normalize(course_code)
    exam_name = __normalize(exam_name)
    if student_id != "ALL":
        try:
            student_id = int(student_id)
        except:
            return "Invalid student ID."
    url = base_url + "/organizations/%s/%s/exams/%s/get_grades/%s" % (organization, course_code, exam_name, student_id)
    return get(url, headers={"Authorization": "Bearer " + token}).json()


@server_check
def getAnswersOfStudent(token, course, exam, student_id,
                        organization=current_organization, base_url=server_address):
    # returns a list: [answer_id, question_id, student_id, given_answer, given_grade or None]
    organization = __normalize(organization)
    course = __normalize(course)
    exam = __normalize(exam)
    url = base_url + "/organizations/%s/%s/exams/%s/get_answers/%s" % (organization, course, exam, student_id)
    return get(url, headers={"Authorization": "Bearer " + token}).json()


@server_check
def getLastActivities(token, username, sign_in=False, organization=current_organization, base_url=server_address):
    url = base_url + "/organizations/%s/%s/" % (organization, username)
    if sign_in:
        url += "last_login"
    else:
        url += "last_activities"
    return get(url, headers={"Authorization": "Bearer " + token}).json()


@server_check
def postExamData(token, course, exam, user_id, key_stream, keystroke=None, memory_usage=None, network_download=None,
                 network_upload=None, organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    course = __normalize(course)
    exam = __normalize(exam)
    data = {"keystroke": keystroke, "memory_usage": memory_usage, "network_download": network_download,
            "network_upload": network_upload, "key_stream": key_stream}
    url = base_url + "/organizations/%s/%s/exams/%s/data/%s" % (organization, course, exam, user_id)
    return put(url, headers={"Authorization": "Bearer " + token}, data=data).json()


@server_check
def extraMaterials(token, course, exam, question_id, file_, purpose, upload=False,
                   organization=current_organization, base_url=server_address):
    purpose = __normalize(purpose)
    if purpose not in ("auto_grade", "reference", "visual_question"):
        return "Wrong purpose!"
    organization = __normalize(organization)
    course = __normalize(course)
    exam = __normalize(exam)
    url = base_url + "/organizations/%s/%s/exams/%s/materials" % (organization, course, exam)
    with open(file_, "rb") as data_f:
        if upload:
            rtn = put(url, files={"file": data_f},
                      data={"question_id": question_id, "purpose": purpose},
                      headers={"Authorization": "Bearer " + token}).json()
        else:
            rtn = None
            pass
    return rtn


@server_check
def getKeyloggerData(token, course, exam, student_id, organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    course = __normalize(course)
    exam = __normalize(exam)
    url = base_url + "/organizations/%s/%s/exams/%s/keystrokes" % (organization, course, exam)
    return get(url, data={"student_id": student_id},
               headers={"Authorization": "Bearer " + token}).json()


@server_check
def giveSecondAccessExam(token, course, exam, student_username,
                         organization=current_organization, base_url=server_address):
    organization = __normalize(organization)
    course = __normalize(course)
    exam = __normalize(exam)
    url = base_url + "/organizations/%s/%s/exams/%s/exceptional_access" % (organization, course, exam)
    return put(url, data={"student_user": student_username}, headers={"Authorization": "Bearer " + token}).json()