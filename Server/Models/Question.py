#-*-coding:utf-8-*-
import json
class Question:
    def __init__(self, tip, subject, text, answer, inputs, outputs, value, tags):
        self.tip = tip
        self.subject = subject
        self.text = text
        self.tags = tags
        self.answer = answer
        self.inputs = inputs
        self.outputs = outputs
        self.value = value
        self.get ={"type": self.tip,
                "subject": self.subject,
                "text": self.text,
                "answer": self.answer,
                "inputs": self.inputs,
                "outputs": self.outputs,
                "value": self.value,
                "tags" : self.tags
                }

    def getString(self):
        return json.dumps(self.get)

    def save(self, db, course_code, organization, exam_code):
        org = organization.replace(" ", "_").lower()
        course_code = course_code.lower().replace(" ", "_")
        command = "USE %s;" %org
        command += "INSERT IGNORE INTO questions (info, examID) select \'%s\' , ExamID from (select exams.ExamID, exams.CourseID, courses.CODE from exams join courses where exams.CourseID = courses.CourseID and exams.ExamID = %d) as T where T.CODE = \'%s\';" %(self.getString(), exam_code, course_code)
        db.execute(command)
        return self

    def save_command(self, course_code, exam_name):
        course_code = course_code.lower().replace(" ", "_")
        command = "INSERT IGNORE INTO questions (info, ExamID) select \'%s\' , ExamID from (select exams.ExamID, exams.CourseID, courses.CODE from exams join courses where exams.CourseID = courses.CourseID and exams.Name = \'%s\') as T where T.CODE = \'%s\';" %(self.getString(), exam_name, course_code)
        return command

    def load(self, db, id, organization):
        org = organization.replace(" ", "_").lower()
        command = "SELECT * FROM %s.questions WHERE questionID = %d;" % (org, int(id))

        data = db.execute(command)[0]
        return json.dumps({
            "question id": data[0],
            "exam id": data[1],
            "info": json.loads(data[2])
        })

    def edit(self, db, id, organization):
        return db.execute("Update %s.questions Set info = '%s' where QuestionID = %d;" % (
        organization, self.getString(), int(id)))
