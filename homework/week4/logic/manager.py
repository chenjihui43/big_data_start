import os
from homework.week4.logic.student import Student
import json
from homework.week4.logic.course import Course


class CourseManager:
    def __init__(self):
        # dict{s_id:student_obj}
        self.students = {}
        self.courses = {}
        self.load_course_data()

    def load_student_data(self):
        # 加载学生数据
        if os.path.exists("week4/data/students.json"):
            with open("week4/data/students.json", "r") as f:
                data = json.load(f)
            for student_dict in data.values():
                student = Student.from_dict(student_dict)
                self.students[student.student_id] = student

    def load_course_data(self):
        # 加载课程数据
        if os.path.exists("../data/courses.json"):
            with open("../data/courses.json", "r", encoding='utf-8') as f:
                data = json.load(f)
            for course_dict in data.values():
                course = Course.from_dict(course_dict)
                self.courses[course.cid] = course

    def save_data(self):
        # 创建顶层字典结构
        data = {}
        for student in self.students:  # 遍历所有学生对象
            # 使用学生ID作为键，学生字典作为值
            data[student.sid] = student.to_dict()
        # 写入JSON文件
        with open("week4/data/students.json", "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_student(self, sid, sname):
        if sid not in self.students:
            self.students[sid] = Student(sid, sname)
            return True, "添加学生成功！"
        else:
            return False, "已存在该学生"

    def add_score(self, sid, cid, score):
        if sid not in self.students:
            return False, "学生不存在"
        if cid not in self.courses:
            return False, "课程不存在"
        student = self.students[sid]
        if cid in student.courses_grade:
            return False, "已存在对输入学生和课程的成绩记录"
        else:
            student.courses_grade[cid] = score
            return True, "成绩添加成功"

    def alter_score(self, sid, cid, score):
        if sid not in self.students:
            return False, "学生不存在"
        if cid not in self.courses:
            return False, "课程不存在"
        student = self.students[sid]
        if cid not in student.courses_grade:
            return False, "该学生这门课的成绩尚未记录"
        else:
            student.courses_grade[cid] = score
            return True, "成绩修改成功"

    def get_student_scores(self, sid):
        student = self.students[sid]
        answer_dict = {}
        for key, value in student.courses_grade.items():
            answer_dict[key] = [value]
        return answer_dict

    def save_student_to_file(self, filename="../data/students.json"):
        """保存数据到文件"""
        # 准备学生数据
        students = {}
        for sid, student in self.students.items():
            students[sid] = student.to_dict()
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(students, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到文件: {filename}")
            return True
        except Exception as e:
            print(f"保存文件时出错: {str(e)}")
            return False

    def load_from_file(self, filename="../data/students.json"):
        """从文件加载数据"""
        if not os.path.exists(filename):
            print(f"文件不存在: {filename}")
            return False
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 加载学生数据
            for sid, student_dict in data.items():
                student = Student.from_dict(student_dict)
                self.students[sid] = student
            print(f"从文件 {filename} 加载了 {len(self.students)} 名学生记录")
            return True
        except Exception as e:
            print(f"加载文件时出错: {str(e)}")
            return False