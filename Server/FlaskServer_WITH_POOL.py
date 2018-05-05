# -*- coding:UTF-8 -*-
from memory_profiler import profile
from flask import Flask, request, jsonify
from Models.MySQLdb_WITH_CONN_POOL import MySQLdb as PooledMySQLdb
from Models.Exam import Exam
from Models.User import *
from Models.Course import Course
from Models.Lecture import *
from Models.External_Functions.decimalEncoder import DecimalEncoder
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
import json, datetime, pickle

app = Flask(__name__)
db = PooledMySQLdb("TestDB")
memory_log = open("memory.log", "w+")
app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = "CHANGE THIS BEFORE DEPLOYMENT ! ! !"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=8)

jwt = JWTManager(app)
expired_token = set()


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


def log_activity(ip, username, endpoint):
    db.execute(
        "INSERT INTO last_activities(Username, IP, Api_Endpoint) VALUES ('%s', '%s', '%s');" % (username, ip, endpoint))
    return

@app.route("/", endpoint="alive")
@profile(stream=memory_log)
def test_connection():
    return jsonify("I am alive!")


@app.route("/organizations", methods=["PUT"], endpoint="register_organization")
@profile(stream=memory_log)
@jwt_required
def signUpOrganization():
    with db:
        if check_auth(get_jwt_identity(), "istanbul_sehir_university", "admin"):
            return jsonify(db.initialize_organization(request.form["data"]))
        else:
            return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>", methods = ["PUT"], endpoint="register_user")
@profile(stream=memory_log)
@jwt_required
def signUpUser(organization):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization ,"admin"):
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
            return rtn


@app.route("/organizations/<string:organization>/<string:username>", methods=["GET"], endpoint="sign_in")
@profile(stream=memory_log)
def signInUser(organization, username):
    with db:
        username = request.authorization["username"]
        password = request.authorization["password"]
        user = User(db, organization, username)
        try:
            if user.verify_password(password):
                rtn = user.get
                rtn.append(organization)
                rtn.append(create_access_token(identity=({"username" : user.username, "role":user.role_name, "time": str(datetime.datetime.today()), "organization": user.organization, "id": user.user_id})))
                log_activity(request.remote_addr, username, request.endpoint)
                return jsonify(rtn)
            else:
                return jsonify("Wrong Password")
        except IndexError:
            return jsonify("Wrong Username")
        except:
            return jsonify("An error occurred")


@app.route("/organizations/<string:organization>/<string:username>/out", methods=["PUT"], endpoint="sign_out")
@profile(stream=memory_log)
@jwt_required
def signOutUser(organization, username):
    with db:
        identity = get_jwt_identity()
        if username != identity["username"] or organization != identity["organization"]:
            return jsonify("Unauthorized access!")
        token = get_raw_jwt()["jti"]
        rtn = jsonify({"Log out status": db.revoke_token(token) is None})
        log_activity(request.remote_addr, username, request.endpoint)
        return rtn


@jwt.token_in_blacklist_loader
@profile(stream=memory_log)
def is_revoked(token):
    with db:
        jti = token["jti"]
        rtn = db.if_token_revoked(jti)
        return rtn

@app.route("/organizations/<string:organization>/<string:course>", methods=['PUT'], endpoint="add_course")
@profile(stream=memory_log)
@jwt_required
def addCourse(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "admin"):
            return jsonify("Unauthorized access!")
        else:
            name = request.form["name"]
            code = request.form["code"]
            lecturers = request.form["lecturers"]
            rtn =  jsonify(Course(db, organization, code).add_course(name, lecturers))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn


@app.route("/organizations/<string:organization>/<string:course>/get", methods=['GET'], endpoint="get_course")
@profile(stream=memory_log)
@jwt_required
def getCourse(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "student"):
            return jsonify("Unauthorized Access.")
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Course(db, organization, course).get_course())
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register/<string:liste>", methods=['PUT'], endpoint="register_student_list")
@profile(stream=memory_log)
@jwt_required
def putStudentList(organization, course, liste):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            if liste == "True":
                rtn = jsonify(Course(db, organization, course).register_student_csv(request.files["liste"], request.form["username"]))
            else:
                rtn = jsonify(Course(db, organization, course).register_student(pickle.loads(request.form["liste"])))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register", methods=['GET'], endpoint="get_student_list")
@profile(stream=memory_log)
@jwt_required
def getStudentList(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Course(db, organization, course).get_course_participants())
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/courses/role=lecturer", methods=["GET"], endpoint="get_courses")
@profile(stream=memory_log)
@jwt_required
def getUserCourseList(organization, username):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            user = Student(db, organization, username)
            rtn = jsonify(user.get_student_courses())
        else:
            user = Lecturer(db, organization, username)
            rtn = jsonify(user.get_lecturer_courses())
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/delete_user", methods=['DELETE'], endpoint="delete_from_course")
@profile(stream=memory_log)
@jwt_required
def deleteStudentFromLecture(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")

        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Course(db, organization, course).delete_student_course(request.form["Student"]))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/edit_password", methods=["PUT"], endpoint="change_password")
@profile(stream=memory_log)
@jwt_required
def changePassword(organization, username):
    with db:
        token = get_jwt_identity()
        user = User(db, token["organization"], token["username"])
        if username != user.username or user.organization != organization:
            return jsonify("Unauthorized access!")
        ismail = request.form["isMail"]
        if ismail == "True":
            ismail = True
        else:
            ismail = False
        rtn = jsonify(user.change_password_or_email(request.form["Password"], request.form["newPassword"], ismail))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/add", methods=["PUT"], endpoint="create_exam")
@profile(stream=memory_log)
@jwt_required
def addExam(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            name = request.form["name"]
            time = request.form["time"]
            duration = request.form["duration"]
            status = request.form["status"]
            exam = Exam(name, organization, db)
            rtn = jsonify(exam.save(course, time, duration, status))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/delete", methods=["DELETE"], endpoint="delete_exam")
@profile(stream=memory_log)
@jwt_required
def deleteExam(organization, course, exam):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Exam(exam, organization, db).delete_exam())
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/", methods=["GET"], endpoint="get_exams_of_lecture")
@profile(stream=memory_log)
@jwt_required
# todo: STUDENT CANNOT REACH QUESTIONS BEFORE EXAM START TIME
def getExamsOfLecture(organization, course):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "student"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Course(db, organization, course).get_exams_of_lecture())
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")

@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>", methods=["GET"], endpoint="get_exam")
@profile(stream=memory_log)
@jwt_required
def getExam(organization, course, name):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "student"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(Exam(name, organization, db).get())
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>/addQuestion", methods=["PUT"], endpoint="add_question")
@profile(stream=memory_log)
@jwt_required
def addQuestionsToExam(organization, course, name):
    with db:
        token = get_jwt_identity()
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            info = json.loads(request.form["data"])
            rtn = Exam(name, organization, db=db).addQuestion(info["type"], info["subject"], info["text"], info["answer"], info["inputs"], info["outputs"], info["value"], info["t"
                                                                                                                                                                                "ags"])
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return jsonify(rtn)
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<question_id>/answers/<string:username>", methods=["PUT"], endpoint="send_answer")
@profile(stream=memory_log)
@jwt_required
def answerExam(organization, course, question_id, username):
    with db:
        token = get_jwt_identity()
        if token["role"] != "student":
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            user = Student(db, organization, username)
            user.add_answer(question_id, request.form["answers"])
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return jsonify("Done")
        return jsonify("Unauthorized access!")



@app.route("/organizations/<string:organization>/<string:username>/pic", methods=["PUT", "GET"], endpoint="profile_picture")
@profile(stream=memory_log)
@jwt_required
def profilePicture(organization, username):
    with db:
        token = get_jwt_identity()
        user = User(db, token["organization"], token["username"])
        if user.username != username and user.organization != organization:
            return jsonify("Unauthorized access!")
        if request.method == "PUT":
            pic = request.files["pic"]
            # cont = request.form["pic"]
            if pic.filename == "":
                return jsonify("No picture selected.")
            rtn = jsonify(user.upload_profile_pic(pic))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        else:
            path = user.get_profile_picture()
            try:
                with open(path, "rb") as f:
                    a = f.read()
                    log_activity(request.remote_addr, token["username"], request.endpoint)
                    return jsonify(pickle.dumps(a))
            except TypeError:
                return jsonify(None)


@app.route("/organizations/<string:organization>/<string:course>/exams/<question_id>/answers/<string:studentUser>/grade", methods=["PUT"], endpoint="grade_answer")
@profile(stream=memory_log)
@jwt_required
def gradeQuestion(organization, course, question_id, studentUser):
    with db:
        token = get_jwt_identity()
        user = Lecturer(db, token["organization"], token["username"])
        if not check_auth(get_jwt_identity(), organization, "lecturer"):
            return "Unauthorized Access"
        if check_lecture_permision(organization, token, course):
            rtn = jsonify(user.grade_answer(question_id, studentUser,request.form["grade"]))
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return rtn
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/<string:question_id>/edit", methods=["PUT"], endpoint="edit_question")
@profile(stream=memory_log)
@jwt_required
def editQuestion(organization, course, exam_name, question_id):
    with db:
        token = get_jwt_identity()
        role = token["role"]
        if role != "lecturer" and check_lecture_permision(organization, token, course):
            return jsonify("Unauthorized access!")
        rtn = jsonify(Exam(exam_name, organization, db).edit_a_question(question_id, json.loads(request.form["data"])))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/more_time", methods=["PUT"], endpoint="add_time_exam")
@profile(stream=memory_log)
@jwt_required
def addTimeToExam(organization, course, exam_name):
    with db:
        token = get_jwt_identity()
        role = token["role"]
        if role != "lecturer" and check_lecture_permision(organization, token, course):
            return jsonify("Unauthorized access!")
        rtn = jsonify(Exam(exam_name, organization, db).add_more_time(request.form["additional_time"]))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/status", methods=["PUT"], endpoint="change_status_exam")
@profile(stream=memory_log)
@jwt_required
def changeStatusOfExam(organization, course, exam_name):
    with db:
        token = get_jwt_identity()
        role = token["role"]
        if role != "lecturer" and check_lecture_permision(organization, token, course):
            return jsonify("Unauthorized access!")
        rtn = jsonify(Exam(exam_name, organization, db).change_status(request.form["status"]))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:username>/reset_password", methods=["GET", "PUT"], endpoint="reset_password")
@profile(stream=memory_log)
def reset_password(organization, username):
    with db:
        user = User(db, organization, username)
        if request.method == "GET":
            rtn = jsonify(user.reset_password())
        else:
            rtn = jsonify(user.check_and_change_password(request.authorization["username"], new_pass=request.authorization["password"]))
        log_activity(request.remote_addr, username, request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/get_grades/<string:student_id>", endpoint="get_grades", methods=["GET"])
@profile(stream=memory_log)
@jwt_required
def get_grades(organization, course, exam_name, student_id):
    token = get_jwt_identity()
    with db:
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return DecimalEncoder().encode(Exam(exam_name, organization, db).get_grades(student_id))
        return "Unauthorized access."


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/get_answers/<string:student_id>", endpoint="get_answers", methods=["GET"])
@jwt_required
def get_answers_of_student(organization, course, exam_name, student_id):
    token = get_jwt_identity()
    with db:
        if not check_auth(token, organization, "lecturer"):
            return jsonify("Unauthorized access!")
        if check_lecture_permision(organization, token, course):
            log_activity(request.remote_addr, token["username"], request.endpoint)
            return jsonify(Exam(exam_name, organization, db).get_answers(student_id))
        return jsonify("Unauthorized access.")

@app.route("/organizations/<string:organization>/<string:username>/<any(last_login, last_activities):endpoint>", endpoint="last_activities", methods=["GET"])
@profile(stream=memory_log)
@jwt_required
def get_last_activities(organization, username, endpoint):
    token = get_jwt_identity()
    with db:
        user = User(db, organization, token["username"])
        rtn = jsonify(user.get_last_activity(endpoint))
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/data/<string:username>", methods=["PUT"], endpoint="exam_data")
@profile(stream=memory_log)
@jwt_required
def exam_data(organization, course, username, exam):
    token = get_jwt_identity()
    username = token["username"]
    with db:
        if not check_auth(token, organization, "student") or not check_lecture_permision(organization, token, course):
            rtn = "Unauthorized access"
        else:
            file_ = request.files["exam_data"]
            Exam(exam, organization, db=db).save_exam_data(username, course, file_)
            rtn = "Done"
    log_activity(request.remote_addr, token["username"], request.endpoint)
    return jsonify(rtn)

@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/materials", methods=["PUT", "GET"], endpoint="extra_materials")
@profile(stream=memory_log)
@jwt_required
def upload_extra_materials(organization, course, exam):
    token = get_jwt_identity()
    with db:
        if not check_auth(token, organization, "lecturer") or not check_lecture_permision(organization, token, course):
            rtn = "Unauthorized access."
        else:
            rtn = Exam(exam, organization, db).upload_extra_materials(request.files["file"],
                                                                      course, exam,
                                                                      request.form["question_id"],
                                                                      request.form["purpose"])
    return jsonify(rtn)


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/keystrokes", methods=["PUT", "GET"], endpoint="keystrokes")
@profile(stream=memory_log)
@jwt_required
def upload_keystroke(organization, course, exam):
    token = get_jwt_identity()
    student = request.form["student_id"]
    with db:
        if request.method == "PUT":
            if not check_lecture_permision(organization, token, course) or not check_auth(token, organization, "student"):
                rtn = "Unauthorized access."
            else:
                rtn = Exam(exam, organization, db).record_live_exam_keystrokes(course, student, request.form["stream"])
        else:
            if not check_lecture_permision(organization, token, course) or not check_auth(token, organization, "lecturer"):
                rtn = "Unauthorized access."
            else:
                rtn = Exam(exam, organization, db).get_live_exam_keystrokes(course, student)

    return jsonify(rtn)


if __name__ == "__main__":
    app.run(host="localhost", port=8888)
