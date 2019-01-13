# -*-coding:utf-8-*-
import hashlib

class Password:
    def __init__(self):
        self.password_hash = None
        pass

    def hash_password(self, password):
        algorithm = hashlib.sha512()
        algorithm.update(password)
        self.password_hash = algorithm.hexdigest()
        return self.password_hash

    def verify_password_hash(self, password, hashed_password):
        password = self.hash_password(password)
        return password == hashed_password
