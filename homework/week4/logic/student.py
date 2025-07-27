class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.courses_grade = {}

    def to_dict(self):
        return {"sid": self.sid, "name": self.name, "courses_grade": self.courses_grade}

    @classmethod
    def from_dict(cls, data):
        """从字典创建学生对象"""
        student = cls(data['sid'], data['name'])
        student.courses_grade = data['courses_grade']
        return student
