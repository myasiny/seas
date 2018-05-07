# -*-coding:utf-8-*-
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
        self.get = {"type": self.tip,
                    "subject": self.subject,
                    "text": self.text,
                    "answer": self.answer,
                    "inputs": self.inputs,
                    "outputs": self.outputs,
                    "value": self.value,
                    "tags": self.tags}

    def get_string(self):
        return json.dumps(self.get)

    def save(self, db, organization, exam_name):
        org = organization.replace(" ", "_").lower()
        command = "USE %s;" % org
        command += "INSERT IGNORE INTO questions(info, ExamID) VALUES " \
                   "('%s', (SELECT e.ExamID from exams e, courses c WHERE c.CourseID = e.CourseID and e.Name = '%s'));"\
                   % (self.get_string(), exam_name)
        db.execute(command)
        return self

    @staticmethod
    def load(db, id_, organization):
        org = organization.replace(" ", "_").lower()
        command = "SELECT * FROM %s.questions WHERE questionID = %d;" % (org, int(id_))

        data = db.execute(command)[0]
        return json.dumps({
            "question id": data[0],
            "exam id": data[1],
            "info": json.loads(data[2])
        })

    def edit(self, db, id_, organization):
        return db.execute("Update %s.questions Set info = '%s' where QuestionID = %d;"
                          % (organization, self.get_string(), int(id_)))
