#-*-coding:utf-8-*-
from Question import Question
import json

class Exam:
    def __init__(self, Name, organization, db=None):
        self.org = organization.replace(" ", "_").lower()
        self.name = Name
        self.db = db

        self.course = None
        self.time = None
        self.duration = None
        self.status = None
        self.ID = None

        self.get()

    def addQuestion(self, tip, subject, text, answer, inputs, outputs, value, tags):
        if self.course is None:
            return None
        question = Question(tip, subject, text, answer, inputs, outputs, value, tags).save(self.db, self.course, self.org, self.ID)
        return question.get

    def addQuestionObject(self, questionObj):
        return questionObj.save(self.db, self.course, self.org, self.ID).get

    def save(self, CourseCode, Time, duration, status="draft"):
        """
            use istanbul_sehir_university;
            insert into exams(Name,Time,CourseID) select 'bioinformatics mt 1', '2018-02-15 10:30:00', ID from courses where courses.CODE = 'eecs_468';
        """
        db = self.db
        self.course = CourseCode.replace(" ", "_").lower()
        self.time = Time
        self.duration = duration
        self.status = status
        command = "USE %s;" % self.org
        command += "insert into exams(Name,Time,Duration, Status, CourseID) " \
                   "select \'%s\', \'%s\', %d, '%s', CourseID " \
                   "from courses where courses.CODE = \'%s\'" \
                   "ON DUPLICATE KEY UPDATE Name = '%s', Time='%s', Duration='%s', Status = '%s';"\
                   % (self.name, self.time, int(self.duration), self.status, self.course, self.name, self.time, self.duration, self.status)

        db.execute(command)
        return db.execute("SELECT ExamID FROM exams WHERE Name = '%s'" % self.name)[0][0]

    def get(self):
        db = self.db
        command = "select time, duration, ExamID from %s.exams where name = '%s'" %(self.org, self.name)
        saved = db.execute(command)
        try:
            self.time = saved[0][0]
            self.duration = saved[0][1]
            c = "SELECT s.Code FROM %s.courses s, %s.exams e where s.CourseID = e.courseID and e.Name = '%s' ;" % (self.org, self.org, self.name)
            c = db.execute(c)[0][0]
            self.course = c
            questions = self.get_questions()
            self.ID = saved[0][2]
            return{
                "Name": self.name,
                "Course": self.course,
                "Time": saved[0][0],
                "Duration": saved[0][1],
                "Questions": questions,
                "ID": saved[0][2]
            }
        except IndexError:
            print "No Exam"
            return "No Exam Named as " + self.name
        except Exception as e:
            print "Error"
            return "Unknown Error for exam " + self.name + " with " + e.message

    def getString(self, db):
        return json.dumps(self.get(db))

    def delete_exam(self):
        organization = self.org
        exam_name = self.name
        try:
            id = self.db.execute("select ExamID from %s.exams where Name = '%s'" % (organization, exam_name))[0][0]
            c = "DELETE FROM %s.exams WHERE ExamID='%s'" %(organization, id)
            return self.db.execute(c)
        except IndexError:
            return "No such an Exam named " + exam_name

    def change_status(self, new_status):
        self.db.execute("Update %s.exams Set Status = '%s' where Name = '%s';" % (self.org, new_status, self.name))

    def add_more_time(self, minutes):
        self.db.execute("Update %s.exams Set Duration = Duration + %d where Name = '%s';" % (self.org, int(minutes), self.name))

    def get_questions(self):
        command = "SELECT info, QuestionID FROM %s.questions join %s.exams where %s.exams.Name = '%s' and %s.questions.examID = %s.exams.examID;" % (
        self.org, self.org, self.org, self.name, self.org, self.org)
        raw_questions = self.db.execute(command)
        questions = {}
        i = 0
        for question in raw_questions:
            i = i + 1
            questions[question[1]] = question[0]
        # for question in self.questions:
        #     i = i + 1
        #     questions[i] = question.get
        return questions

    def edit_a_question(self, question_id, info):
        try:
            q = Question(info["type"], info["subject"], info["text"], info["answer"], info["inputs"], info["outputs"],info["value"], info["tags"])
            return q.edit(self.db, question_id, self.org)

        except KeyError as k:
            return k.message
