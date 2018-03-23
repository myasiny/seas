#-*-coding:utf-8-*-
from Question import Question
import json

class Exam:
    def __init__(self, Name, organization, db=None):
        self.org = organization.replace(" ", "_").lower()
        self.name = Name
        self.db = db
        self.db.execute("USE %s;" % self.org)

    def addQuestion(self, tip, subject, text, answer, inputs, outputs, value, tags):
        question = Question(tip, subject, text, answer, inputs, outputs, value, tags).save(self.db, self.org, self.name)
        return question.get

    def addQuestionObject(self, questionObj):
        return questionObj.save(self.db, self.course, self.org, self.ID).get

    def save(self, CourseCode, Time, duration, status="draft"):
        db = self.db
        course = CourseCode.replace(" ", "_").lower()
        command = ""
        command += "insert into exams(Name,Time,Duration, Status, CourseID) " \
                   "select \'%s\', \'%s\', %d, '%s', CourseID " \
                   "from courses where courses.CODE = \'%s\'" \
                   "ON DUPLICATE KEY UPDATE Name = '%s', Time='%s', Duration='%s', Status = '%s';"\
                   % (self.name, Time, int(duration), status, course, self.name, Time, duration, status)
        db.execute(command)
        return "Done"

    def get(self):
        db = self.db
        command = "select q.info, q.QuestionID, c.Code, e.* from questions q JOIN (courses c, exams e) ON c.CourseID = e.courseID AND e.Name = '%s' AND q.ExamID = e.ExamID;" %self.name
        saved = db.execute(command)
        course, exam_id, exam_name, course_id, time, duration, status = saved[0][2:]
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
                "Status": status
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
