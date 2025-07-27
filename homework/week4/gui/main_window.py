import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from homework.week4.logic.manager import CourseManager


class StudentManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("学生成绩管理系统")
        master.geometry("600x500")  # 增大主窗口尺寸

        # 设置字体
        self.title_font = ("微软雅黑", 16, "bold")
        self.button_font = ("微软雅黑", 12)
        self.dialog_font = ("微软雅黑", 11)

        # 初始化管理器
        self.manager = CourseManager()

        # 创建主框架
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题标签 - 增大字号
        self.label = tk.Label(
            main_frame,
            text="学生成绩管理系统",
            font=self.title_font,
            pady=15
        )
        self.label.pack()

        # 功能按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # 功能按钮 - 增大按钮尺寸
        buttons = [
            ("添加学生", self.add_student),
            ("添加成绩", self.add_score),
            ("修改成绩", self.modify_score),
            ("查看学生成绩", self.view_scores),
            ("保存数据到文件", self.save_data),
            ("从文件加载数据", self.load_data),
            ("退出系统", self.exit_app)
        ]

        # 创建两列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.button_font,
                height=2,
                width=20
            )
            btn.grid(row=row, column=col, padx=10, pady=8, sticky="ew")

        # 设置网格列权重
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def add_student(self):
        """添加学生功能"""
        sid = simpledialog.askstring(
            "添加学生",
            "请输入学号:",
            parent=self.master
        )
        if not sid:
            return

        sname = simpledialog.askstring(
            "添加学生",
            "请输入姓名:",
            parent=self.master
        )
        if not sname:
            return

        success, msg = self.manager.add_student(sid, sname)
        if success:
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("错误", msg)

    def add_score(self):
        """添加成绩功能"""
        sid = simpledialog.askstring(
            "添加成绩",
            "请输入学号:",
            parent=self.master
        )
        if not sid:
            return

        cid = simpledialog.askstring(
            "添加成绩",
            "请输入课程ID:",
            parent=self.master
        )
        if not cid:
            return

        score = simpledialog.askfloat(
            "添加成绩",
            "请输入分数:",
            parent=self.master
        )
        if score is None:
            return

        success, msg = self.manager.add_score(sid, cid, score)
        if success:
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("错误", msg)

    def modify_score(self):
        """修改成绩功能"""
        sid = simpledialog.askstring(
            "修改成绩",
            "请输入学号:",
            parent=self.master
        )
        if not sid:
            return

        cid = simpledialog.askstring(
            "修改成绩",
            "请输入课程ID:",
            parent=self.master
        )
        if not cid:
            return

        score = simpledialog.askfloat(
            "修改成绩",
            "请输入新分数:",
            parent=self.master
        )
        if score is None:
            return

        success, msg = self.manager.alter_score(sid, cid, score)
        if success:
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("错误", msg)

    def view_scores(self):
        """查看学生成绩功能 - 优化显示窗口"""
        sid = simpledialog.askstring(
            "查看成绩",
            "请输入学号:",
            parent=self.master
        )
        if not sid:
            return

        try:
            scores = self.manager.get_student_scores(sid)
            if not scores:
                messagebox.showinfo("信息", "该学生没有成绩记录")
                return

            # 构建成绩显示文本
            result = f"学号: {sid}\n\n课程成绩:\n"
            for cid, score_list in scores.items():
                result += f"课程 {cid}: {score_list[0]}\n"

            # 在新窗口中显示成绩 - 增大窗口尺寸
            score_window = tk.Toplevel(self.master)
            score_window.title(f"学生 {sid} 成绩单")
            score_window.geometry("500x400")  # 固定窗口大小

            # 添加滚动文本框
            text_frame = tk.Frame(score_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            text_area = scrolledtext.ScrolledText(
                text_frame,
                wrap=tk.WORD,
                width=50,
                height=20,
                font=self.dialog_font  # 这里可以设置字体
            )
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, result)
            text_area.config(state=tk.DISABLED)

            # 添加关闭按钮
            close_btn = tk.Button(
                score_window,
                text="关闭",
                command=score_window.destroy,
                font=self.button_font,
                width=15
            )
            close_btn.pack(pady=10)

        except KeyError:
            messagebox.showerror("错误", "找不到该学生")

    def save_data(self):
        """保存数据到文件功能"""
        # 询问用户是否要保存
        confirm = messagebox.askyesno(
            "确认保存",
            "确定要保存所有数据吗？",
            parent=self.master,
            icon="question"
        )
        if not confirm:
            return

        # 调用manager的保存方法
        success = self.manager.save_student_to_file()
        if success:
            messagebox.showinfo("保存成功", "数据已成功保存到文件")
        else:
            messagebox.showerror("保存失败", "数据保存失败，请检查日志")

    def load_data(self):
        """从文件加载数据功能"""
        # 警告用户加载数据会覆盖当前数据
        confirm = messagebox.askyesno(
            "确认加载",
            "加载数据将覆盖当前所有未保存的修改。\n确定要继续吗？",
            parent=self.master,
            icon="warning"
        )
        if not confirm:
            return

        # 调用manager的加载方法
        success = self.manager.load_from_file()
        if success:
            messagebox.showinfo("加载成功", "数据已成功从文件加载")
        else:
            messagebox.showerror("加载失败", "数据加载失败，请检查日志")

    def exit_app(self):
        """退出应用程序 - 添加确认提示"""
        confirm = messagebox.askyesno(
            "确认退出",
            "确定要退出系统吗？",
            parent=self.master,
            icon="question"
        )
        if confirm:
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerGUI(root)
    root.mainloop()
