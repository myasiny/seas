from requests import put, get, ConnectionError, Timeout

import re


def testConnection(URL):
    try:
        return True
    except ConnectionError:
        return False


def addOrganization(URL, Organization):
    Organization = Organization.replace(" ", "_").lower()
    url = URL+"/organizations"
    return put(url, data={"data": Organization}).json()


def addUser(URL, organization, id, name, surname, username, password, Email, Department ,role="student"):
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
                        }).json()


def signIn(URL, organization, username, password):
    url = URL+"/organizations/%s/%s" %(organization.replace(" ", "_").lower(), username)
    return get(url, data={
                        "Username": username,
                        "Password": password
                        }).json()


def signOut(URL, organization, username):
    url = URL + "/organizations/%s/%s/out" % (organization.replace(" ", "_").lower(), username)
    return get(url, data={
        "Username": username,
    }).json()


def addCourse(URL, organization, courseName, courseCode, *lecturer_users):
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
        "lecturers": lecturers}
               ).json()


def addLecturerToCourse():
    pass

def getCourse(URL, organization, courseCode):
    courseCode = re.sub(r'[^\w\s]', '_', courseCode).replace(" ", "_").lower()
    organization = organization.replace(" ", "_").lower()
    url = URL + "/organizations/%s/%s" % (organization, courseCode)
    return get(url, data={
    }).json()
