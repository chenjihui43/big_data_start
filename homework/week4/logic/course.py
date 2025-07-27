class Course:
    def __init__(self, cid, name, credit):
        self.cid = cid
        self.name = name
        self.credit = credit

    @classmethod
    def from_dict(cls, data):
        """从字典创建学生对象"""
        course = cls(data['cid'], data['name'],data['credit'])
        return course