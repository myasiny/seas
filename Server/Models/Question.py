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
        self.test_cases = {}
        for i in range(len(self.inputs)):
            self.test_cases[str(self.inputs[i])] = self.outputs[i]
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
        tags = ""
        for i in self.tags:
            tags += "%s, " % i
        tags = tags[:-1]
        org = organization.replace(" ", "_").lower()
        command = "USE %s;" % org
        command += "INSERT INTO questions(Type, Subject, Body, Answer, Test_Cases, Value, Tags, ExamID) VALUES" \
                   " ('%s', '%s', '%s', '%s', \"%s\", '%s', '%s', (SELECT e.ExamID from exams e, courses c " \
                   "WHERE c.CourseID = e.CourseID and e.Name = '%s'));" % (self.tip, self.subject, self.text,
                                                                           self.answer, json.dumps(self.test_cases).
                                                                           replace("'", "STR-JSON"),
                                                                           self.value, tags, exam_name)
        db.execute(command)
        return self

    @staticmethod
    def load(db, id_, organization):
        org = organization.replace(" ", "_").lower()
        command = "SELECT * FROM %s.questions WHERE questionID = %d;" % (org, int(id_))
        data = db.execute(command)[0]
        info = {}
        info.setdefault("inputs", [])
        info.setdefault("outputs", [])
        col_names = ["subject", "tags", "type", "text", "answer", "inputs", "outputs"]
        # todo: UPDATE 3 WHEN PUBLISHING
        values = data[3:]
        for i in range(len(values)):
            info[col_names[i]] = values[i]
            if col_names[i] == "inputs":
                a = json.loads(values[i])
                for key, value in a.items():
                    info[col_names[i]].append(key)
                    info[col_names[i+1]].append(value)

        return json.dumps({
            "question id": data[0],
            "exam id": data[1],
            "info": info
        })

    def edit(self, db, id_, organization):
        tags = ""
        for i in self.tags:
            tags += "%s, " % i
        tags = tags[:-1]
        command = "Update %s.questions Set type = '%s', subject = '%s', Body = '%s', Answer = '%s', " \
                  "Test_Cases = '%s', Value = %s, Tags = '%s' where QuestionID = %d;"\
                  % (organization, self.tip, self.subject, self.text, self.answer,
                     json.dumps(self.test_cases).replace("'", "STR-JSON"), self.value, tags, int(id_))
        print command
        return db.execute(command)
