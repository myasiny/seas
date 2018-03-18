#-*-coding:utf-8-*-
from passlib.apps import custom_app_context as pwd_context

class Password():
    def __init__(self):
        pass

    def hashPassword(self, password):
        self.password_hash = pwd_context.encrypt(password, )
        return self.password_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def verify_password_hash(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)
