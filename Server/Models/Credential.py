# -*-coding:utf-8-*-
from Password import Password


class Credential:
    def __init__(self, username, password, db, org):
        self.username = username
        self.password = password
        self.db = db
        self.org = org
        pass

    def get_password(self):
        return self.db.execute("SELECT Password FROM %s_members WHERE Username = '%s'" %(self.org, self.username))[0]

    def check_password(self):
        return Password().verify_password_hash(Password().hash_password(self.password), self.get_password())

    def get_role(self):
        self.db.execute("SELECT Role FROM %s_members WHERE Username='%s'" %(self.org, self.username))

    def get_permissions(self):
        pass
