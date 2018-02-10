# -*- coding:UTF-8 -*-

from flask import Flask, request, jsonify
from Models import MySQLdb, Password, Credential, Question, Exam
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore, roles_accepted
from flask_security.utils import login_user
from SessionManager import db_session, init_db
from SessionModels import User, Role
import json
import datetime, time

app = Flask(__name__)
db = MySQLdb("TestDB", app)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "super_secret"

user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)


roles = {"admin": user_datastore.find_or_create_role("admin"),
         "superuser": user_datastore.find_or_create_role("superuser"),
         "student": user_datastore.find_or_create_role("student"),
         "lecturer": user_datastore.find_or_create_role("lecturer")}



def create_user(username, domain, role, password, current_ip = None):
    init_db()
    user = user_datastore.find_user(username=username)
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user is None:
        user_datastore.create_user(username=username, domain=domain, roles=[role], password=password,
                                   current_login_ip=current_ip,
                                   current_login_at=today, active=0)
    else:
        date = user.current_login_at
        ip = user.current_login_ip

        user_datastore.activate_user(user)
        user.last_login_at = date
        user.last_login_ip = ip
        user.current_login_ip = current_ip
        user.current_login_at = today
    db_session.commit()


@app.route("/")
def test_connection():
    return jsonify("I am alive!")


@app.route("/organizations", methods=["PUT"])
def signUpOrganization():
    # user = user_datastore.find_user(current_login_ip = request.remote_addr, username=request.form["user"])
    # if user is not None and user.is_active and user.has_role(user_datastore.find_role("admin")):
    #     return jsonify(db.initialize_organization(request.form["data"]))
    # else:
    #     return jsonify("Unauthorized process!!")
    return jsonify(db.initialize_organization(request.form["data"]))


@app.route("/organizations/<string:organization>", methods = ["PUT"])
# @roles_accepted("admin")
def signUpUser(organization):
    passwd = Password().hashPassword(request.form["Password"])
    username = request.form["Username"]
    role = request.form["Role"].lower()
    command = "Insert into %s.members(PersonID, Role, Name, Surname, Username, Password, Email, Department) " \
              "values(%s, '%d', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (organization,
                 request.form["ID"],
                 int(db.execute("SELECT RoleID FROM %s.roles WHERE Role = '%s'" % (
                 organization, role))[0][0]),
                 request.form["Name"],
                 request.form["Surname"],
                 username,
                 passwd,
                 request.form["Email"],
                 request.form["Department"]
                 )

    rtn = jsonify(db.execute(command))
    create_user(username=username, domain=organization, role = role, password=passwd, current_ip=None)
    return rtn


@app.route("/organizations/<string:organization>/<string:username>", methods=["GET"])
# @app.before_first_request
def signInUser(organization, username):
    organization = organization.replace(" ", "_").lower()
    username = request.form["Username"]
    try:
        passwd = db.execute("select Password from %s.members where Username = '%s'"
                            % (organization, username))[0][0]
        if Password().verify_password_hash(request.form["Password"], passwd):
            rtn = list(db.execute("select Username, Name, Surname, PersonID, Role, Email, Department "
                                  "from %s.members where Username=('%s')" % (organization, username))[0])
            rtn[4] = db.execute("SELECT Role FROM %s.roles WHERE RoleID = '%s'" % (organization, rtn[4]))[0][0]
            rtn.append(organization)
            # login_user(user_datastore.find_user(username=username), remember=True)
            return jsonify(rtn)

        else:
            return jsonify("Wrong Password")
    except IndexError:
        return jsonify("Wrong Username")


@app.route("/organizations/<string:organization>/<string:username>/out", methods=["GET", "PUT"])
def signOutUser(organization, username):
    organization = organization.replace(" ", "_").lower()
    user = user_datastore.find_user(username=username, domain=organization)
    return jsonify(user_datastore.deactivate_user(user))


@app.route("/organizations/<string:organization>/<string:course>", methods=['PUT'])
def addCourse(organization, course):
    name = request.form["name"]
    code = request.form["code"]
    lecturers = request.form["lecturers"]
    return jsonify(db.add_course(organization, name, code, lecturers))


@app.route("/organizations/<string:organization>/<string:course>/get", methods=['GET'])
def getCourse(organization, course):

    return jsonify(db.get_course(organization, course))


@app.route("/organizations/<string:organization>/<string:course>/register/<string:liste>", methods=['PUT'])
def putStudentList(organization, course, liste):

    return jsonify(db.registerStudentCSV(request.files["liste"], organization, course, request.form["username"]))


@app.route("/organizations/<string:organization>/<string:course>/register", methods=['GET'])
def getStudentList(organization, course):
    return jsonify(db.get_course_participants(course, organization))


@app.route("/organizations/<string:organization>/<string:username>/courses/role=lecturer", methods=["GET"])
def getLecturerCourseList(organization, username):
    return jsonify(db.get_lecturer_courses(organization, username))


@app.route("/organizations/<string:organization>/<string:course>/delete_user", methods=['DELETE'])
def deleteStudentFromLecture(organization, course):
    return jsonify(db.delete_student_course(organization, course, request.form["Student"]))


@app.route("/organizations/<string:organization>/<string:username>/edit_password", methods=["PUT"])
def changePassword(organization, username):
    ismail = request.form["isMail"]
    if ismail == "True":
        ismail = True
    else:
        ismail = False
    return jsonify(db.changePasswordOREmail(organization, username, request.form["Password"], request.form["newPassword"], email=ismail))


@app.route("/organizations/<string:organization>/<string:course>/exams/add", methods=["PUT"])
def addExam(organization, course):
    name = request.form["name"]
    time = request.form["time"]
    duration = request.form["duration"]
    questions = json.loads(request.form["questions"])
    exam = Exam(name, course, time, duration, organization)
    for j in questions:
        i=questions[j]
        exam.addQuestion(
            i["type"],
            i["subject"],
            i["text"],
            i["answer"],
            i["inputs"],
            i["outputs"],
            i["value"],
            i["tags"])
    return jsonify(exam.save(db))

@app.route("/organizations/<string:organization>/<string:course>/exams/", methods=["GET"])
def getExamsOfLecture(organization, course):
    pass

@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>", methods=["GET"])
def getExam(organization, course, name):
    exam = Exam(name, course, None, None, organization)
    return jsonify(exam.get(db))

from json import loads
if __name__ == "__main__":
    app.run(host="10.50.81.24", port=8888)
    # a = Question("classic", "history", "who is the founder of TR?", "Ataturk", [(1,2),(2,3)], [(3),(5)], 30, "mustafa", "kemal")
    # e = Exam("bioinformatics mt 1", "eecs 468", "17.2.2018.10.00.00", 60, "istanbul sehir university")
    # e.addQuestionObject(a)
    # e.addQuestion("truefalse", "history", "Ottomans were Muslims.", "true", "", "", 30, "ottomans", "muslim")
    # print e.get()
    # print e.getString()
    # print loads(a.load(db, 3, "istanbul sehir university"))["info"]["tags"]
    # print a.load(db, 3, "istanbul sehir university")
    # print e.get(db)
    pass