# -*- coding:UTF-8 -*-

from flask import Flask, request, jsonify
from Models.MySQLdb_WITH_CONN_POOL import MySQLdb as PooledMySQLdb
from Models.Exam import Exam
from Models.User import *
from Models.Course import Course
from Models.Lecture import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
import json, datetime, pickle

app = Flask(__name__)
db = PooledMySQLdb("TestDB")

app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "./uploads/"
app.config["JWT_SECRET_KEY"] = "CHANGE THIS BEFORE DEPLOYMENT ! ! !"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
if app.config["DEBUG"]:
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
else:
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=18)

jwt = JWTManager(app)
expired_token = set()


def connection_wrapper(func):
    def get_connection_from_pool(*args, **kwargs):
        db.get_connection()
        rtn = func(*args, **kwargs)
        db.close_connection()
        return rtn
    return get_connection_from_pool


def check_auth(token, allowed_organization, min_allowed_role):
    role_ranks = {
        "student": ["superuser", "admin", "lecturer", "student"],
        "lecturer": ["superuser", "admin", "lecturer"],
        "admin": ["superuser", "admin"],
        "superuser": ["superuser"]
                  }

    allowed_roles = role_ranks[min_allowed_role]
    user = token["username"]
    role = token["role"]
    token_time = token["time"]
    organization = token["organization"]
    return role in allowed_roles and organization == allowed_organization


def check_lecture_permision(organization, token, course):
    if token["role"] == "student":
        courses = Student(db, organization, token["username"]).get_student_courses()
    else:
        courses = Lecturer(db, organization, token["username"]).get_lecturer_courses()

    course_dict = {}
    for value, key in courses:
        course_dict[key] = value

    if course not in course_dict:
        return False

    return True


@app.route("/")
def test_connection():
    return jsonify("I am alive!")


@app.route("/organizations", methods=["PUT"])
@jwt_required
def signUpOrganization():
    db.get_connection()
    if check_auth(get_jwt_identity(), "istanbul_sehir_university", "admin"):
        db.close_connection()
        return jsonify(db.initialize_organization(request.form["data"]))
    else:
        db.close_connection()
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>", methods = ["PUT"])
@jwt_required
def signUpUser(organization):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization ,"admin"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    else:
        passwd = Password().hash_password(request.form["Password"])
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
        db.close_connection()
        return rtn


@app.route("/organizations/<string:organization>/<string:username>", methods=["GET"])
# todo: Fatihgulmez , separate data manipulation and access from views!!!
def signInUser(organization, username):
    db.get_connection()
    organization = organization.replace(" ", "_").lower()
    username = request.authorization["username"]
    password = request.authorization["password"]
    user = User(db, organization, username)
    try:
        if user.verify_password(password):
            rtn = user.get
            rtn.append(organization)
            rtn.append(create_access_token(identity=({"username" : user.username, "role":user.role_name, "time": str(datetime.datetime.today()), "organization": user.organization, "id": user.user_id})))
            try:
                with open(user.profile_pic_path, "rb") as f:
                    pic = f.read()
                rtn.append(pickle.dumps(pic))
            except IOError:
                rtn.append(None)
            db.close_connection()
            return jsonify(rtn)
        else:
            db.close_connection()
            return jsonify("Wrong Password")
    except IndexError:
        db.close_connection()
        return jsonify("Wrong Username")


@app.route("/organizations/<string:organization>/<string:username>/out", methods=["PUT"])
@jwt_required
def signOutUser(organization, username):
    db.get_connection()
    identity = get_jwt_identity()
    if username != identity["username"] or organization != identity["organization"]:
        db.close_connection()
        return jsonify("Unauthorized access!")
    token = get_raw_jwt()["jti"]
    rtn = jsonify({"Log out status": db.revoke_token(token) is not None})
    db.close_connection()
    return rtn


@jwt.token_in_blacklist_loader
def is_revoked(token):
    db.get_connection()
    jti = token["jti"]
    rtn = db.if_token_revoked(jti)
    db.close_connection()
    return rtn


@app.route("/organizations/<string:organization>/<string:course>", methods=['PUT'])
@jwt_required
def addCourse(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "admin"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    else:
        name = request.form["name"]
        code = request.form["code"]
        lecturers = request.form["lecturers"]
        rtn =  jsonify(Course(db, organization, code).add_course(name, lecturers))
        db.close_connection()
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/get", methods=['GET'])
@jwt_required
def getCourse(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        db.close_connection()
        return jsonify("Unauthorized Access.")

    if check_lecture_permision(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_course())
        db.close_connection()
        return rtn

    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register/<string:liste>", methods=['PUT'])
@jwt_required
def putStudentList(organization, course, liste):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        if liste == "True":
            rtn = jsonify(Course(db, organization, course).register_student_csv(request.files["liste"], request.form["username"]))
            db.close_connection()
            return rtn
        else:
            rtn = jsonify(Course(db, organization, course).register_student(pickle.loads(request.form["liste"])))
            db.close_connection()
            return rtn

    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register", methods=['GET'])
@jwt_required
def getStudentList(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_course_participants())
        db.close_connection()
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/courses/role=lecturer", methods=["GET"])
@jwt_required
def getUserCourseList(organization, username):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        user = Student(db, organization, username)
        rtn = jsonify(user.get_student_courses())
        db.close_connection()
        return rtn
    else:
        user = Lecturer(db, organization, username)
        rtn = jsonify(user.get_lecturer_courses())
        db.close_connection()
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/delete_user", methods=['DELETE'])
@jwt_required
def deleteStudentFromLecture(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")

    if check_lecture_permision(organization, token, course):
        rtn = jsonify(Course(db, organization, course).delete_student_course(request.form["Student"]))
        db.close_connection()
        return rtn

    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/edit_password", methods=["PUT"])
@jwt_required
def changePassword(organization, username):
    db.get_connection()
    token = get_jwt_identity()
    user = User(db, token["organization"], token["username"])
    if username != user.username or user.organization != organization:
        db.close_connection()
        return jsonify("Unauthorized access!")
    ismail = request.form["isMail"]
    if ismail == "True":
        ismail = True
    else:
        ismail = False

    rtn = jsonify(user.change_password_or_email(request.form["Password"], request.form["newPassword"], ismail))
    db.close_connection()
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/add", methods=["PUT"])
@jwt_required
def addExam(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        name = request.form["name"]
        time = request.form["time"]
        duration = request.form["duration"]
        status = request.form["status"]
        exam = Exam(name, organization, db)
        rtn = jsonify(exam.save(course, time, duration, status))
        db.close_connection()
        return rtn
    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/delete", methods=["DELETE"])
@jwt_required
def deleteExam(organization, course, exam):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        rtn = jsonify(Exam(exam, organization, db).delete_exam())
        db.close_connection()
        return rtn

    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/", methods=["GET"])
@jwt_required
# todo: STUDENT CANNOT REACH QUESTIONS BEFORE EXAM START TIME
def getExamsOfLecture(organization, course):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_exams_of_lecture())
        db.close_connection()
        return rtn
    db.close_connection()
    return jsonify("Unauthorized access!")

@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>", methods=["GET"])
@jwt_required
def getExam(organization, course, name):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        exam = Exam(name, organization, db)
        rtn = jsonify(exam.get())
        db.close_connection()
        return rtn
    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>/addQuestion", methods=["PUT"])
@jwt_required
def addQuestionsToExam(organization, course, name):
    db.get_connection()
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        info = json.loads(request.form["data"])
        rtn = Exam(name, organization, db=db).addQuestion(info["type"], info["subject"], info["text"], info["answer"], info["inputs"], info["outputs"], info["value"], info["tags"])
        db.close_connection()
        return jsonify(rtn)
    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<question_id>/answers/<string:username>", methods=["PUT"])
@jwt_required
def answerExam(organization, course, question_id, username):
    db.get_connection()
    token = get_jwt_identity()
    if token["role"] != "student":
        db.close_connection()
        return jsonify("Unauthorized access!")
    if check_lecture_permision(organization, token, course):
        db.get_connection()
        user = Student(db, organization, username)
        rtn = jsonify(user.add_answer(question_id, request.form["answers"]))
        db.close_connection()
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/pic", methods=["PUT", "GET"])
@jwt_required
def profilePicture(organization, username):
    db.get_connection()
    token = get_jwt_identity()
    user = User(db, token["organization"], token["username"])
    if user.username != username and user.organization != organization:
        db.close_connection()
        return jsonify("Unauthorized access!")
    if request.method == "PUT":
        pic = request.files["pic"]
        cont = request.form["pic"]
        if pic.filename == "":
            db.close_connection()
            return jsonify("No picture selected.")
        rtn = jsonify(user.upload_profile_pic(pic, pickle.loads(cont), app.config["UPLOAD_FOLDER"]))
        db.close_connection()
        return rtn
    else:
        path = user.get_profile_picture()
        with open(path, "rb") as f:
            a = f.read()
        db.close_connection()
        return jsonify(pickle.dumps(a))


@app.route("/organizations/<string:organization>/<string:course>/exams/<question_id>/answers/<string:studentUser>/grade", methods=["PUT"])
@jwt_required
def gradeQuestion(organization, course, question_id, studentUser):
    db.get_connection()
    token = get_jwt_identity()
    user = Lecturer(db, token["organization"], token["username"])
    if not check_auth(get_jwt_identity(), organization, "lecturer"):
        db.close_connection()
        return "Unauthorized Access"
    if check_lecture_permision(organization, token, course):
        rtn = jsonify(user.grade_answer(question_id, request.form["grade"]))
        db.close_connection()
        return rtn
    db.close_connection()
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/<string:question_id>/edit", methods=["PUT"])
@jwt_required
def editQuestion(organization, course, exam_name, question_id):
    db.get_connection()
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permision(organization, token, course):
        db.close_connection()
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).edit_a_question(question_id, json.loads(request.form["data"])))
    db.close_connection()
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/more_time", methods=["PUT"])
@jwt_required
def addTimeToExam(organization, course, exam_name):
    db.get_connection()
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permision(organization, token, course):
        db.close_connection()
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).add_more_time(request.form["additional_time"]))
    db.close_connection()
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/status", methods=["PUT"])
@jwt_required
def changeStatusOfExam(organization, course, exam_name):
    db.get_connection()
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permision(organization, token, course):
        db.close_connection()
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).change_status(request.form["status"]))
    db.close_connection()
    return rtn


@app.route("/organizations/<string:organization>/<string:username>/reset_password", methods=["GET", "PUT"])
def reset_password(organization, username):
    db.get_connection()
    user = User(db, organization, username)
    if request.method == "GET":
        rtn = jsonify(user.reset_password())
    else:
        rtn = jsonify(user.check_and_change_password(request.authorization["username"], new_pass=request.authorization["password"]))
    db.close_connection()
    return rtn


if __name__ == "__main__":
    app.run(host="localhost", port=8888, threaded=True)
