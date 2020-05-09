from uuid import uuid4


class User(object):
    def __init__(self, name, age):
        self.id = str(uuid4())
        self.name = name
        self.age = age
