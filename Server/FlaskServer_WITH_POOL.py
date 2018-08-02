# -*- coding:UTF-8 -*-

from memory_profiler import profile
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
from Models.MySQLdb_WITH_CONN_POOL import MySQLdb as PooledMySQLdb
from Models.Exam import Exam
from Models.User import *
from Models.Course import Course
from Models.External_Functions.decimalEncoder import DecimalEncoder
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
import json
import datetime
import pickle

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
    role = token["role"]
    organization = token["organization"]
    return role in allowed_roles and organization == allowed_organization


def check_lecture_permission(organization, token, course):
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


def log_activity(ip, username, endpoint, desc=None):
    db.log_activity(username, ip, endpoint, desc)


def db_connector(func):
    def wrapper(*args, **kwargs):
        with db:
            return func(*args, **kwargs)
    return wrapper


@app.route("/", endpoint="alive")
@profile(stream=memory_log)
def test_connection():
    return jsonify("I am alive!")


@app.route("/organizations", methods=["PUT"], endpoint="register_organization")
@profile(stream=memory_log)
@jwt_required
@db_connector
def sign_up_organization():
    if check_auth(get_jwt_identity(), "istanbul_sehir_university", "admin"):
        return jsonify(db.initialize_organization(request.form["data"]))
    else:
        return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>",
           methods=["PUT"], endpoint="register_user")
@profile(stream=memory_log)
@jwt_required
@db_connector
def sign_up_user(organization):
    token = get_jwt_identity()
    if not check_auth(token, organization, "admin"):
        return jsonify("Unauthorized access!")
    else:
        return jsonify(db.sign_up_user(organization, request))


@app.route("/organizations/<string:organization>/<string:username>",
           methods=["GET"], endpoint="sign_in")
@profile(stream=memory_log)
@db_connector
def sign_in_user(organization, username):
    username = request.authorization["username"]
    password = request.authorization["password"]
    user = User(db, organization, username)
    try:
        if user.verify_password(password):
            rtn = user.get
            rtn.append(organization)
            rtn.append(create_access_token(identity=(
                {
                    "username": user.username,
                    "fullname": "%s %s" % (user.name, user.surname),
                    "role": user.role_name,
                    "time": str(datetime.datetime.today()),
                    "organization": user.organization,
                    "id": user.user_id
                }
            )))
            log_activity(request.remote_addr, username, request.endpoint)
            return jsonify(rtn)
        else:
            return jsonify("Wrong Password")
    except IndexError:
        return jsonify("Wrong Username")
    except:
        return jsonify("An error occurred")


@app.route("/organizations/<string:organization>/<string:username>/out",
           methods=["PUT"], endpoint="sign_out")
@profile(stream=memory_log)
@jwt_required
@db_connector
def sign_out_user(organization, username):
    identity = get_jwt_identity()
    if username != identity["username"] or organization != identity["organization"]:
        return jsonify("Unauthorized access!")
    token = get_raw_jwt()["jti"]
    log_activity(request.remote_addr, username, request.endpoint)
    rtn = jsonify({"Log out status": db.revoke_token(token) is None})
    return rtn


@jwt.token_in_blacklist_loader
@profile(stream=memory_log)
@db_connector
def is_revoked(token):
    jti = token["jti"]
    rtn = db.if_token_revoked(jti)
    return rtn


@app.route("/organizations/<string:organization>/<string:course>",
           methods=['PUT'], endpoint="add_course")
@profile(stream=memory_log)
@jwt_required
@db_connector
def add_course(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "admin"):
        return jsonify("Unauthorized access!")
    else:
        name = request.form["name"]
        code = request.form["code"]
        lecturers = request.form["lecturers"]
        rtn = jsonify(Course(db, organization, code).add_course(name, lecturers))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn


@app.route("/organizations/<string:organization>/<string:course>/get",
           methods=['GET'], endpoint="get_course")
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_course(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        return jsonify("Unauthorized Access.")
    if check_lecture_permission(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_course())
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register/<string:liste>",
           methods=['PUT'], endpoint="register_student_list")
@profile(stream=memory_log)
@jwt_required
@db_connector
def register_student_list(organization, course, liste):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        if liste == "True":
            rtn = jsonify(
                Course(db, organization, course).register_student_csv(request.files["liste"], token["fullname"])
            )
        else:
            rtn = jsonify(Course(db, organization, course).register_student(pickle.loads(request.form["liste"])))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/register",
           methods=['GET'], endpoint="get_student_list")
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_student_list(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_course_participants())
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/courses/role=lecturer",
           methods=["GET"], endpoint="get_courses")
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_user_course_list(organization, username):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        user = Student(db, organization, username)
        rtn = jsonify(user.get_student_courses())
    else:
        user = Lecturer(db, organization, username)
        rtn = jsonify(user.get_lecturer_courses())
    log_activity(request.remote_addr, token["username"], request.endpoint)
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/delete_user",
           methods=['DELETE'], endpoint="delete_from_course")
@profile(stream=memory_log)
@jwt_required
@db_connector
def delete_student_from_lecture(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")

    if check_lecture_permission(organization, token, course):
        rtn = jsonify(Course(db, organization, course).delete_student_course(request.form["Student"]))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/edit_password",
           methods=["PUT"], endpoint="change_password")
@profile(stream=memory_log)
@jwt_required
@db_connector
def change_password(organization, username):
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


@app.route("/organizations/<string:organization>/<string:course>/exams/add",
           methods=["PUT"], endpoint="create_exam")
@profile(stream=memory_log)
@jwt_required
@db_connector
def add_exam(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        name = request.form["name"]
        time = request.form["time"]
        duration = request.form["duration"]
        status = request.form["status"]
        exam = Exam(name, organization, db)
        rtn = jsonify(exam.save(course, time, duration, status))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    print "that"
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/delete",
           methods=["DELETE"], endpoint="delete_exam")
@profile(stream=memory_log)
@jwt_required
@db_connector
def delete_exam(organization, course, exam):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        rtn = jsonify(Exam(exam, organization, db).delete_exam())
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/",
           methods=["GET"], endpoint="get_exams_of_lecture")
@profile(stream=memory_log)
@jwt_required
@db_connector
# todo: STUDENT CANNOT REACH QUESTIONS BEFORE EXAM START TIME
def get_exams_of_lecture(organization, course):
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        rtn = jsonify(Course(db, organization, course).get_exams_of_lecture(token["role"] == "student"))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>",
           methods=["GET"], endpoint="get_exam")
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_exam(organization, course, name):
    token = get_jwt_identity()
    if not check_auth(token, organization, "student"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        exam = Exam(name, organization, db)
        rtn = exam.get()
        if token["role"] == "student":
            if not exam.check_first_enter(token["username"]):
                return jsonify("You already sit the exam!")
            print rtn["Status"]!="active"
            if not (rtn["Status"] == "active" or rtn["Status"] == "graded"):
                return jsonify("Cannot access to exam.")
        log_activity(request.remote_addr, token["username"], request.endpoint, name)
        return jsonify(rtn)
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:name>/add_question",
           methods=["PUT"], endpoint="add_question")
@profile(stream=memory_log)
@jwt_required
@db_connector
def add_questions_to_exam(organization, course, name):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        info = json.loads(request.form["data"])
        rtn = Exam(name, organization, db=db).add_question(
            info["type"], info["subject"], info["text"], info["answer"],
            info["inputs"], info["outputs"], info["value"], info["t""ags"]
        )
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return jsonify(rtn)
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<question_id>/answers/<string:username>",
           methods=["PUT"], endpoint="send_answer")
@profile(stream=memory_log)
@jwt_required
@db_connector
def answer_exam(organization, course, question_id, username):
    token = get_jwt_identity()
    if token["role"] != "student":
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        user = Student(db, organization, username)
        user.add_answer(question_id, request.form["answers"])
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return jsonify("Done")
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:username>/pic",
           methods=["PUT", "GET"], endpoint="profile_picture")
@profile(stream=memory_log)
@jwt_required
@db_connector
def profile_picture(organization, username):
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
            response = send_from_directory("", path)
            return response
        except TypeError:
            return jsonify(None)


@app.route("/organizations/<string:organization>/<string:course>/"
           "exams/<question_id>/answers/<student_user>/grade",
           methods=["PUT"], endpoint="grade_answer")
@profile(stream=memory_log)
@jwt_required
@db_connector
def grade_question(organization, course, question_id, student_user):
    token = get_jwt_identity()
    user = Lecturer(db, token["organization"], token["username"])
    if not check_auth(get_jwt_identity(), organization, "lecturer"):
        return "Unauthorized Access"
    if check_lecture_permission(organization, token, course):
        rtn = jsonify(user.grade_answer(question_id, student_user, request.form["grade"]))
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return rtn
    return jsonify("Unauthorized access!")


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/<string:question_id>/edit",
           methods=["PUT"], endpoint="edit_question")
@profile(stream=memory_log)
@jwt_required
@db_connector
def edit_question(organization, course, exam_name, question_id):
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permission(organization, token, course):
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).edit_a_question(question_id, json.loads(request.form["data"])))
    log_activity(request.remote_addr, token["username"], request.endpoint)
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/more_time",
           methods=["PUT"], endpoint="add_time_exam")
@profile(stream=memory_log)
@jwt_required
@db_connector
def add_time_to_exam(organization, course, exam_name):
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permission(organization, token, course):
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).add_more_time(request.form["additional_time"]))
    log_activity(request.remote_addr, token["username"], request.endpoint)
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam_name>/status",
           methods=["PUT"], endpoint="change_status_exam")
@profile(stream=memory_log)
@jwt_required
@db_connector
def change_status_of_exam(organization, course, exam_name):
    token = get_jwt_identity()
    role = token["role"]
    if role != "lecturer" and check_lecture_permission(organization, token, course):
        return jsonify("Unauthorized access!")
    rtn = jsonify(Exam(exam_name, organization, db).change_status(request.form["status"]))
    log_activity(request.remote_addr, token["username"], request.endpoint)
    return rtn


@app.route("/organizations/<string:organization>/<string:username>/reset_password",
           methods=["GET", "PUT"], endpoint="reset_password")
@profile(stream=memory_log)
@db_connector
def reset_password(organization, username):
    user = User(db, organization, username)
    if request.method == "GET":
        rtn = jsonify(user.reset_password())
    else:
        rtn = jsonify(user.check_and_change_password(
            request.authorization["username"],
            new_pass=request.authorization["password"])
        )
    log_activity(request.remote_addr, username, request.endpoint)
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/"
           "<string:exam_name>/get_grades/<string:student_id>",
           endpoint="get_grades", methods=["GET"])
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_grades(organization, course, exam_name, student_id):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return DecimalEncoder().encode(Exam(exam_name, organization, db).get_grades(student_id))
    return "Unauthorized access."


@app.route("/organizations/<string:organization>/<string:course>"
           "/exams/<string:exam_name>/get_answers/<string:student_id>",
           endpoint="get_answers", methods=["GET"])
@jwt_required
@db_connector
def get_answers_of_student(organization, course, exam_name, student_id):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        log_activity(request.remote_addr, token["username"], request.endpoint)
        return jsonify(Exam(exam_name, organization, db).get_answers(student_id, exam_name))
    return jsonify("Unauthorized access.")


@app.route("/organizations/<string:organization>/<string:username>/"
           "<any(last_login, last_activities):endpoint>",
           endpoint="last_activities", methods=["GET"])
@profile(stream=memory_log)
@jwt_required
@db_connector
def get_last_activities(organization, username, endpoint):
    token = get_jwt_identity()
    user = User(db, organization, token["username"])
    rtn = jsonify(user.get_last_activity(endpoint))
    return rtn


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/data/<string:username>",
           methods=["PUT"], endpoint="exam_data")
@profile(stream=memory_log)
@jwt_required
@db_connector
def exam_data(organization, course, username, exam):
    token = get_jwt_identity()
    username = token["username"]
    if not check_auth(token, organization, "student") or not check_lecture_permission(organization, token, course):
        rtn = "Unauthorized access"
    else:
        data = request.form
        Exam(exam, organization, db=db).save_exam_data(username, course, data)
        rtn = "Done"
    return jsonify(rtn)


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/keystrokes",
           methods=["GET"], endpoint="keystrokes")
@profile(stream=memory_log)
@jwt_required
@db_connector
def upload_keystroke(organization, course, exam):
    token = get_jwt_identity()
    student = request.form["student_id"]
    if not check_lecture_permission(organization, token, course) or not check_auth(token, organization, "lecturer"):
        rtn = "Unauthorized access."
    else:
        rtn = Exam(exam, organization, db).get_live_exam_keystrokes(course, student)
    return jsonify(rtn)


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/materials",
           methods=["PUT", "GET"], endpoint="extra_materials")
@profile(stream=memory_log)
@jwt_required
@db_connector
def upload_extra_materials(organization, course, exam):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer") or not check_lecture_permission(organization, token, course):
        rtn = "Unauthorized access."
    else:
        rtn = Exam(exam, organization, db).upload_extra_materials(request.files["file"],
                                                                  course, exam,
                                                                  request.form["question_id"],
                                                                  request.form["purpose"])
    return jsonify(rtn)


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/exceptional_access",
           endpoint="second_access", methods=["PUT"])
@profile(stream=memory_log)
@jwt_required
@db_connector
def give_second_access_to_exam(organization, course, exam):
    token = get_jwt_identity()
    if not check_auth(token, organization, "lecturer"):
        return jsonify("Unauthorized access!")
    if check_lecture_permission(organization, token, course):
        exam = Exam(exam, organization, db)
        return jsonify(exam.give_second_access(request.form["student_user"]))


##########
@app.route("/organizations/<string:organization>/<string:course>/stats", methods=['PUT'])
def upload_stats(organization, course, student, data):
    """
    This method is to store statistics in server side.
    :param organization: It's organization name.
    :param course: It's course code.
    :param student: It's student id.
    :param data: It's statistics data.
    :return:
    """

    with open("stats\{org}-{crs}-{std}.txt".format(org=organization, crs=course, std=student), "w+") as f:
        for key, value in data.iteritems():
            f.write(key + "*[SEAS-EQUAL]*" + value + "\n")
        f.close()
    return jsonify("Ok")


@app.route("/organizations/<string:organization>/<string:course>/stats", methods=['GET'])
def get_stats(organization, course, student):
    """
    This method is to get statistics to client side.
    :param organization: It's organization name.
    :param course: It's course code.
    :param student: It's student id.
    :return:
    """

    if student is None:
        return jsonify({"TODO": 0})

    with open("stats\{org}-{crs}-{std}.txt".format(org=organization, crs=course, std=student), "r") as f:
        lines = f.readlines()
        data = {}
        for i in lines:
            pair = i.split("*[SEAS-EQUAL]*")
            data[pair[0]] = pair[1]
        f.close()
    return jsonify(data)


@app.route("/organizations/<string:organization>/<string:course>/exams/<string:exam>/screenshots", methods=['PUT'])
def upload_ss(organization, course, exam, student, data):
    """
    This method is to analyze screenshots in server side.
    :param organization: It's organization name.
    :param course: It's course code.
    :param exam: It's exam name.
    :param student: It's student id.
    :param data: It's statistics data.
    :return:
    """

    result = Exam(exam, organization, db).screenshots_analyzer(data, course, exam, student)
    return jsonify(result)
##########


if __name__ == "__main__":
    app.run(host="localhost", port=8888, threaded=True)
