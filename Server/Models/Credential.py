#-*-coding:utf-8-*-
from Password import Password

class Credential:
    def __init__(self, username, password, db, org):
        self.username = username
        self.password = password
        self.db = db
        self.org = org
        pass

    def getPassword(self):
        return self.db.execute("SELECT Password FROM %s_members WHERE Username = '%s'" %(self.org, self.username))[0]

    def checkPassword(self):
        return Password().verify_password_hash(Password().hash_password(self.password), self.getPassword())

    def getRole(self):
        self.db.execute("SELECT Role FROM %s_members WHERE Username='%s'" %(self.org, self.username))

    def getPermissions(self):
        pass
