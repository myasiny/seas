#-*-coding:utf-8-*-
from Question import Question
import json, threading, os
from werkzeug.utils import secure_filename

class Exam:
    def __init__(self, Name, organization, db=None):
        self.org = organization
        self.name = Name
        self.db = db
        self.db.execute("USE %s;" % self.org)

    def addQuestion(self, tip, subject, text, answer, inputs, outputs, value, tags):
        question = Question(tip, subject, text, answer, inputs, outputs, value, tags).save(self.db, self.org, self.name)
        return question.get

    def addQuestionObject(self, questionObj):
        return questionObj.save(self.db, self.course, self.org, self.ID).get

    def save(self, CourseCode, Time, duration, status="draft", timezone="+03:00"):
        db = self.db
        course = CourseCode.replace(" ", "_").lower()
        proc = "%s.create_exam" % self.org
        db.cursor.callproc(str(proc), args=(self.name, course, Time, duration, status,timezone,))
        command = "DROP EVENT IF EXISTS %s_start;DROP EVENT IF EXISTS %s_stop;" %(self.name, self.name)
        command +="CREATE EVENT %s_start ON SCHEDULE AT date_add('%s', INTERVAL 0 MINUTE) DO UPDATE exams SET Status='active' WHERE exams.Name='%s';" \
                  "CREATE EVENT %s_stop ON SCHEDULE AT date_add('%s', INTERVAL %d MINUTE )DO UPDATE exams SET Status='finished' WHERE exams.Name='%s';" \
        % (self.name, Time, self.name, self.name, Time, int(duration), self.name)

        for com in command.split(";"):
            if len(com)>=1:
                db.execute(com+";")
        return "Done"

    def get(self):
        db = self.db
        try:
            command = "select q.info, q.QuestionID, c.Code, e.* from questions q JOIN (courses c, exams e) ON c.CourseID = e.courseID AND e.Name = '%s' AND q.ExamID = e.ExamID;" %self.name
            saved = db.execute(command)
            course, exam_id, exam_name, course_id, time, duration, status, timezone = saved[0][2:]
        except IndexError:
            try:
                command = "SELECT c.Code, e.* FROM exams e, courses c WHERE e.Name = '%s' and e.CourseID = c.CourseID" %self.name
                saved = db.execute(command)
                course, exam_id, exam_name, course_id, time, duration, status, timezone = saved[0][:8]
                saved = []
            except IndexError: #
                return "No Exam."

        try:
            questions = {}
            counter = 1
            for question in saved:
                question_info = json.loads(question[0])
                question_info["ID"] = question[1]
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
                "Timezone": timezone
            }
        except IndexError:
            return "No Exam Named as " + self.name

    def getString(self, db):
        return json.dumps(self.get())

    def delete_exam(self):
        organization = self.org
        exam_name = self.name
        try:
            c = "DELETE FROM %s.exams WHERE Name='%s'" %(organization, exam_name)
            return self.db.execute(c)
        except IndexError:
            return "No such an Exam named " + exam_name

    def change_status(self, new_status):
        self.db.execute("Update exams Set Status = '%s' where Name = '%s';" % (new_status, self.name))

    def add_more_time(self, minutes):
        self.db.execute("Update exams Set Duration = Duration + %d where Name = '%s';" % (int(minutes), self.name))
        start, dur = self.db.execute("Select Time, Duration from exams where Name = '%s'" %self.name)[0]
        self.db.execute("alter event %s_stop ON SCHEDULE AT date_add('%s', INTERVAL %d MINUTE);" %(self.name, start, int(dur)))

    def get_questions(self):
        command = "SELECT info, QuestionID FROM questions WHERE ExamID =  (SELECT ExamID from exams where Name = '%s');" % (self.name)
        raw_questions = self.db.execute(command)
        questions = {}
        i = 0
        for question in raw_questions:
            i = i + 1
            questions[question[1]] = question[0]
        return questions

    def edit_a_question(self, question_id, info):
        try:
            q = Question(info["type"], info["subject"], info["text"], info["answer"], info["inputs"], info["outputs"],info["value"], info["tags"])
            return q.edit(self.db, question_id, self.org)

        except KeyError as k:
            return k.message

    def get_grades(self, student_id):
        if student_id == "ALL":
            rtn = self.db.execute("select any_value(m.Username) as Username, sum(a.grade) as Grade from answers a, questions q, members m, exams e where e.Name='%s' and q.ExamID = e.ExamID and q.QuestionID = a.questionID and m.PersonID = a.studentID GROUP BY studentID;" %self.name)
        else:
            rtn = self.db.execute("select any_value(m.Username) as Username, sum(a.grade) as Grade from answers a, questions q, members m, exams e where e.Name='%s' and a.studentId = %d and q.ExamID = e.ExamID and q.QuestionID = a.questionID and m.PersonID = a.studentID GROUP BY a.studentID;" % (self.name, int(student_id)))
        return rtn

    def get_answers(self, student_id):
        rtn = self.db.execute("SELECT * FROM answers WHERE studentID = %s;" %student_id)
        return rtn

    def save_exam_data(self, username, course, data):
        base_path = "uploads/%s/courses/%s/exams/%s/user_data/" %(self.org, course, self.name)
        path= base_path + "%s.json" % username
        data_ = json.load(data)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        json.dump(data_, open(path, "w"))
        return

    def upload_extra_materials(self, file_, course, exam, question_id, purpose):
        if purpose not in ("auto_grade", "reference", "visual_question"):
            return "Purpose invalid"
        base_path= "uploads/%s/courses/%s/exams/%s/materials/%s/%s/" % (self.org, course, exam,question_id, purpose)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        path = base_path + secure_filename(file_.filename)
        with open(path, "wb") as ff_:
            data = None
            while data != "":
                data = file_.read()
                ff_.write(data)
        return "Done"

    def record_live_exam_keystrokes(self, course, student_id, stream):
        base_path = "uploads/%s/courses/%s/exams/%s/keystroke/" % (self.org, course, self.name)
        path = base_path + student_id + ".keystroke"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        if os.path.exists(path):
            open_mode = "a"
        else:
            open_mode = "w"
        print open_mode
        with open(path, open_mode) as f:
            f.write(stream)

        return "Done"

    def get_live_exam_keystrokes(self, course, student_id):
        path = "uploads/%s/courses/%s/exams/%s/keystroke/%s.keystroke" % (self.org, course, self.name, student_id)
        if os.path.exists(path):
            return open(path, "r").readlines()
        else:
            return
