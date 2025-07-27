import json
import os


class Student:
    """学生类，包含学号、姓名和选修课程信息"""

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}  # 格式: {课程ID: 分数}

    def add_course_grade(self, course_id, grade):
        """添加课程成绩"""
        course_id = int(course_id)
        self.courses[course_id] = grade

    def calculate_average(self, course_catalog):
        """计算加权平均分"""
        total_points = 0
        total_credits = 0
        for course_id, grade in self.courses.items():
            course = course_catalog[int(course_id)]
            _, _, credit = course
            total_points += credit * grade
            total_credits += credit
        return total_points / total_credits

    def to_dict(self):
        """转换为字典格式用于序列化"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'courses': self.courses
        }


    @classmethod
    def from_dict(cls, data):
        """从字典创建学生对象"""
        student = cls(data['student_id'], data['name'])
        # 将 courses 的键转换为整数
        student.courses = {int(k): v for k, v in data['courses'].items()}
        return student


class StudentManagementSystem:
    """学生管理系统"""
    course_catalog = {
        1: (1, "证券投资分析", 1),
        2: (2, "金融风险管理", 2),
        3: (3, "商务数据分析", 2),
        4: (4, "属性数据分析", 2),
        5: (5, "数据挖掘与机器学习", 1),
        6: (6, "贝叶斯统计", 2),
        7: (7, "金融工程", 2),
        8: (8, "分布式统计计算", 2),
        9: (9, "大数据计算机基础", 1),
        10: (10, "金融机构与市场", 1),
        11: (11, "深度学习与应用", 2)
    }

    def __init__(self):
        self.students = {}  # 格式: {学号: Student对象}

    def display_courses(self):
        """显示所有可用课程"""
        print("\n可用课程列表:")
        print("-" * 50)
        print(f"{'课程ID':<10}{'课程名称':<25}{'学分':<10}")
        print("-" * 50)
        for course_id in self.course_catalog:
            triple = self.course_catalog[course_id]
            _, name, credit = triple
            print(f"{course_id:<10}{name:<25}{credit:<10}")
        print("-" * 50)

    def add_student(self, student_id, name):
        """添加新学生"""
        try:
            student_id = int(student_id)
        except ValueError:
            print("错误：学号必须是整数！")
            return False

        if student_id in self.students:
            print(f"学号 {student_id} 已存在！")
            return False

        self.students[student_id] = Student(student_id, name)
        print(f"学生 {name} 添加成功！")
        return True

    def record_grade(self):
        self.display_courses()
        student_id = input("请输入学号: ").strip()
        course_id = input("请输入课程ID: ").strip()
        grade = input("请输入分数: ").strip()
        """记录课程成绩"""
        try:
            student_id = int(student_id)
            course_id = int(course_id)
            grade = int(grade)
        except ValueError:
            print("错误：学号、课程ID和分数必须是数字！")
            return False

        if student_id not in self.students:
            print(f"学号 {student_id} 不存在！")
            return False

        if course_id not in self.course_catalog:
            print(f"课程ID {course_id} 不存在！")
            return False

        if not 0 <= grade <= 100:
            print("错误：分数必须在0-100之间！")
            return False

        self.students[student_id].add_course_grade(course_id, grade)
        course_name = self.course_catalog[course_id][1]
        print(f"课程成绩记录成功: {course_name} - 分数: {grade}")
        return True

    def save_to_file(self, filename="student_data.json"):
        """保存数据到文件"""
        # 准备课程数据 - 直接使用元组值
        course_data = {}
        for cid, triple in self.course_catalog.items():
            # 三元组格式: (course_id, name, credit)
            course_data[cid] = {
                'course_id': triple[0],
                'name': triple[1],
                'credit': triple[2]
            }

        # 准备学生数据
        student_data = [s.to_dict() for s in self.students.values()]
        data = {
            'courses': course_data,
            'students': student_data
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到文件: {filename}")
            return True
        except Exception as e:
            print(f"保存文件时出错: {str(e)}")
            return False

    def load_from_file(self, filename="student_data.json"):
        """从文件加载数据"""
        if not os.path.exists(filename):
            print(f"文件不存在: {filename}")
            return False
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 加载课程数据 - 恢复为元组格式
            self.course_catalog = {}
            for cid, course_dict in data['courses'].items():
                cid_int = int(cid)
                # 创建元组 (course_id, name, credit)
                self.course_catalog[cid_int] = (
                    course_dict['course_id'],
                    course_dict['name'],
                    course_dict['credit']
                )

            # 加载学生数据
            self.students = {}
            for student_dict in data['students']:
                student = Student.from_dict(student_dict)
                self.students[student.student_id] = student

            print(f"从文件 {filename} 加载了 {len(self.students)} 名学生记录")
            return True
        except Exception as e:
            print(f"加载文件时出错: {str(e)}")
            return False

    def query_student(self, student_id):
        """查询学生记录"""
        try:
            student_id = int(student_id)
        except ValueError:
            print("错误：学号必须是整数！")
            return

        student = self.students.get(student_id)
        if not student:
            print(f"学号 {student_id} 不存在！")
            return

        print("\n" + "=" * 60)
        print(f"学生信息: 学号: {student.student_id} 姓名: {student.name}")
        print("-" * 60)
        print(f"{'课程ID':<10}{'课程名称':<25}{'学分':<10}{'分数':<10}")
        print("-" * 60)

        for course_id, grade in student.courses.items():
            course = self.course_catalog.get(course_id)
            if course:
                _, name, credit = course
                print(f"{course_id:<10}{name:<25}{credit:<10}{grade:<10}")

        avg_grade = student.calculate_average(self.course_catalog)
        print("-" * 60)
        print(f"加权平均成绩: {avg_grade:.2f}")
        print("=" * 60 + "\n")


def display_menu():
    """显示系统菜单"""
    print("\n" + "=" * 30)
    print("学生选修课程成绩管理系统")
    print("=" * 30)
    print("1. 添加新学生")
    print("2. 记录课程成绩")
    print("3. 显示所有课程")
    print("4. 保存数据到文件")
    print("5. 从文件加载数据")
    print("6. 查询学生记录")
    print("7. 退出系统")
    print("=" * 30)


def main():
    """主程序入口"""
    system = StudentManagementSystem()

    while True:
        display_menu()
        choice = input("请输入选项: ").strip()

        if choice == '1':  # 添加新学生
            student_id = input("请输入学号: ").strip()
            name = input("请输入姓名: ").strip()
            system.add_student(student_id, name)

        elif choice == '2':  # 记录课程成绩
            system.record_grade()

        elif choice == '3':  # 显示所有课程
            system.display_courses()

        elif choice == '4':  # 保存数据
            system.save_to_file()


        elif choice == '5':  # 加载数据
            success = system.load_from_file()
            if success:
                print("✅ 数据加载成功！")
            else:
                print("❌ 数据加载失败，请确认文件是否存在或检查文件格式。")

        elif choice == '6':  # 查询学生记录
            student_id = input("请输入学号: ").strip()
            system.query_student(student_id)

        elif choice == '7':  # 退出系统
            # 退出前保存数据
            system.save_to_file()
            print("感谢使用，再见！")
            break
        else:
            print("无效选项，请重新输入！")


if __name__ == "__main__":
    main()
