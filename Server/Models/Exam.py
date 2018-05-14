# -*-coding:utf-8-*-
from Question import Question
import json
import threading
import os
from werkzeug.utils import secure_filename
from mysql.connector import DatabaseError

KEYSTREAM_DELIMITER = "<<S|E|A|S>>*!KEYSTREAM_DELIMITER!*"


class Exam:
    def __init__(self, name, organization, db=None):
        self.org = organization
        self.name = name
        self.db = db
        self.db.execute("USE %s;" % self.org)

    def add_question(self, tip, subject, text, answer, inputs, outputs, value, tags):
        question = Question(tip, subject, text, answer, inputs, outputs, value, tags).save(self.db, self.org, self.name)
        return question.get

    def save(self, course_code, time, duration, status="draft", timezone="+03:00"):
        db = self.db
        course = course_code.replace(" ", "_").lower()
        procedure = "%s.create_exam" % self.org
        db.cursor.callproc(str(procedure), args=(self.name, course, time, duration, status, timezone,))
        command = "DROP EVENT IF EXISTS %s_start;DROP EVENT IF EXISTS %s_stop;" %(self.name, self.name)
        command += "CREATE EVENT %s_start ON SCHEDULE AT date_add('%s', INTERVAL 0 MINUTE) " \
                   "DO UPDATE exams SET Status='active' WHERE exams.Name='%s';" \
                   "CREATE EVENT %s_stop ON SCHEDULE AT date_add('%s', INTERVAL %d MINUTE )" \
                   "DO UPDATE exams SET Status='finished' WHERE exams.Name='%s';"\
                   % (self.name, time, self.name, self.name, time, int(duration), self.name)

        for com in command.split(";"):
            if len(com) >= 1:
                db.execute(com+";")
        return "Done"

    def get(self):
        db = self.db
        command = "SELECT c.Code, e.* FROM exams e, courses c WHERE e.Name = '%s' and e.CourseID = c.CourseID" \
                  % self.name
        saved = db.execute(command)
        course, exam_id, exam_name, course_id, time, duration, status, timezone = saved[0][:8]

        command = "select QuestionID, ExamID, Subject, Tags, Type, Body, Answer, Test_Cases, Value " \
                  "from questions where ExamID = '%s';" % exam_id
        questions_raw = db.execute(command)

        try:
            counter = 1
            questions = dict()
            for question in questions_raw:
                question_info = dict()
                question_info["ID"] = question[0]
                question_info["ExamID"] = question[1]
                question_info["Subject"] = question[2]
                question_info["Tags"] = question[3]
                question_info["Type"] = question[4]
                question_info["Text"] = question[5]
                question_info["Answer"] = question[6]
                try:
                    print type(question[7]), question[7]
                    question_info["Test_Cases"] = json.loads(question[7].replace("STR-JSON", "'"))
                except TypeError:
                    question_info["Test_Cases"] = None
                except AttributeError:
                    question_info["Test_Cases"] = None
                questions[counter] = question_info
                counter += 1
            return{
                "Name": exam_name,
                "Course": course,
                "Time": time,
                "Duration": duration,
                "Questions": questions,
                "ID": exam_id,
                "Status": status,
                "Timezone": timezone}
        except IndexError:
            return "No Exam Named as " + self.name

    def get_string(self):
        return json.dumps(self.get())

    def delete_exam(self):
        organization = self.org
        exam_name = self.name
        try:
            return self.db.execute("DELETE FROM %s.exams WHERE Name='%s'" % (organization, exam_name))
        except IndexError:
            return "No such an Exam named " + exam_name

    def change_status(self, new_status):
        self.db.execute("Update exams Set Status = '%s' where Name = '%s';" % (new_status, self.name))
        if new_status == "active":
            dur = self.get()["Duration"]
            command = "Drop Event %s_start;" % self.name
            try:
                self.db.execute(command)
            except DatabaseError:
                pass
            command = "Alter Event %s_stop On Schedule At date_add(now(), Interval %s Minute)" % (self.name, dur)

            try:
                self.db.execute(command)
            except DatabaseError:
                command = "Create Event %s_stop On Schedule At date_add(now(), Interval %s Minute) " \
                          "Do Update exams set Status = 'not_graded' where name = '%s'" % (self.name, self.name, dur)
                self.db.execute(command)

    def add_more_time(self, minutes):
        self.db.execute("Update exams Set Duration = Duration + %d where Name = '%s';" % (int(minutes), self.name))
        start, dur = self.db.execute("Select Time, Duration from exams where Name = '%s'" % self.name)[0]
        self.db.execute("alter event %s_stop ON SCHEDULE AT date_add('%s', INTERVAL %d MINUTE);"
                        % (self.name, start, int(dur)))

    def get_questions(self):
        command = "SELECT info, QuestionID FROM questions WHERE " \
                  "ExamID = (SELECT ExamID from exams where Name = '%s');" % self.name
        raw_questions = self.db.execute(command)
        questions = {}
        i = 0
        for question in raw_questions:
            i = i + 1
            questions[question[1]] = question[0]
        return questions

    def edit_a_question(self, question_id, info):
        try:
            q = Question(info["type"], info["subject"], info["text"], info["answer"],
                         info["inputs"], info["outputs"], info["value"], info["tags"])
            return q.edit(self.db, question_id, self.org)

        except KeyError as k:
            return k.message

    def get_grades(self, student_id):
        if student_id == "ALL":
            rtn = self.db.execute("select any_value(m.Username) as Username, "
                                  "sum(a.grade) as Grade from answers a, questions q, members m, exams e where "
                                  "e.Name='%s' and q.ExamID = e.ExamID and "
                                  "q.QuestionID = a.questionID and m.PersonID = a.studentID "
                                  "GROUP BY studentID;" % self.name)
        else:
            rtn = self.db.execute("select any_value(m.Username) as Username, "
                                  "sum(a.grade) as Grade from answers a, questions q, members m, exams e where "
                                  "e.Name='%s' and a.studentId = %d and q.ExamID = e.ExamID and "
                                  "q.QuestionID = a.questionID and m.PersonID = a.studentID "
                                  "GROUP BY a.studentID;" % (self.name, int(student_id)))
        return rtn

    def get_answers(self, student_id, exam_name):
        rtn = self.db.execute("SELECT a.* FROM answers a "
                              "JOIN exams e ON a.examID = e.ExamID "
                              "where a.studentID = %s and e.Name = '%s';"
                              % (student_id, exam_name))
        return rtn

    def save_exam_data(self, student_id, course, data):
        base_path = "uploads/%s/courses/%s/exams/%s/" % (self.org, course, self.name)
        key_stream = data.pop("key_stream")

        # Exam data save
        path = base_path + "user_data/%s.json" % student_id
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        if os.path.exists(path):
            data_ = json.load(open(path, "r"))
        else:
            data_ = {}
        for key in data:
            data_["exam_data"].setdefault(key, [])
            data_["exam_data"][key].append(data[key])
        json.dump(data_, open(path, "w"))

        # Key stream save
        path = base_path + "key_streams/%s.keystream" % student_id
        if os.path.exists(path):
            o = "a"
        else:
            o = "w"
        with open(path, o) as key_stream_file:
            key_stream_file.write(key_stream)
            key_stream_file.write(KEYSTREAM_DELIMITER)
        return

    def upload_extra_materials(self, file_, course, exam, question_id, purpose):
        if purpose not in ("auto_grade", "reference", "visual_question"):
            return "Purpose invalid"
        base_path = "/var/www/SEAS/uploads/%s/courses/%s/exams/%s/materials/%s/%s/" \
                    % (self.org, course, exam, question_id, purpose)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        path = base_path + secure_filename(file_.filename)
        with open(path, "wb") as ff_:
            data = None
            while data != "":
                data = file_.read()
                ff_.write(data)
        return "Done"

    def get_live_exam_keystrokes(self, course, student_id):
        path = "uploads/%s/courses/%s/exams/%s/keystroke/%s.keystroke" % (self.org, course, self.name, student_id)
        if os.path.exists(path):
            return open(path, "r").read().split(KEYSTREAM_DELIMITER)
        else:
            return

    def check_first_enter(self, username):
        check = self.db.execute("SELECT Time FROM last_activities WHERE Username = '%s' and Description = '%s'"
                                % (username, self.name))
        try:
            check = check[0]
            check = self.db.execute("SELECT * FROM exam_exceptions WHERE username = '%s' and exam_name = '%s'"
                                    % (username, self.name))
            try:
                check[0]
                self.db.execute("DELETE FROM exam_exceptions WHERE username = '%s' and exam_name = '%s'"
                                % (username, self.name))
                return True
            except IndexError:
                return False
        except IndexError:
            return True

    def give_second_access(self, student_username):
        self.db.execute("INSERT INTO exam_exceptions(username, exam_name) VALUES ('%s', '%s')"
                        % (student_username, self.name))
        return "Done"
