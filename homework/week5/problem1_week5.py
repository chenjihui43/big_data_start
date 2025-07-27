import sys
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QLineEdit,
    QMessageBox, QFileDialog, QGroupBox, QSplitter, QHeaderView, QFormLayout,
    QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

import matplotlib

matplotlib.use('QtAgg')
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# 学生数据模型
class StudentData:
    def __init__(self):
        self.data = pd.DataFrame(columns=[
            '学号', '姓名', '性别', '年龄', '班级',
            '语文', '数学', '英语', '物理', '化学', '生物', '总分'
        ])

    def load_data(self, file_path):
        for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
            try:
                self.data = pd.read_csv(file_path, encoding=encoding)
                self._calculate_total()
                return True
            except UnicodeDecodeError:
                continue
        try:
            self.data = pd.read_csv(file_path)
            self._calculate_total()
            return True
        except Exception as e:
            print(f"加载数据错误: {e}")
            return False

    def save_data(self, file_path, encoding='utf_8_sig'):
        try:
            self.data.to_csv(file_path, index=False, encoding=encoding)
            return True
        except Exception as e:
            print(f"保存数据错误: {e}")
            return False

    def _calculate_total(self):
        subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
        if not self.data.empty:
            self.data['总分'] = self.data[subjects].sum(axis=1)

    def add_student(self, student_info):
        try:
            self.data = pd.concat([self.data, pd.DataFrame([student_info])], ignore_index=True)
            self._calculate_total()
            return True
        except Exception as e:
            print(f"添加学生错误: {e}")
            return False

    def remove_student(self, student_id):
        try:
            if student_id in self.data['学号'].values:
                self.data = self.data[self.data['学号'] != student_id]
                return True
            return False
        except Exception as e:
            print(f"删除学生错误: {e}")
            return False

    def get_data(self):
        return self.data.copy()


# 数据分析类
class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def subject_summary(self, subject):
        if subject not in self.data.columns:
            return None
        data = self.data[subject].dropna()
        return {
            '平均分': round(data.mean(), 2),
            '最高分': data.max(),
            '最低分': data.min(),
            '及格率': round((data >= 60).mean() * 100, 2),
            '优秀率': round((data >= 85).mean() * 100, 2)
        } if not data.empty else None

    def gender_comparison(self, subject):
        if '性别' not in self.data.columns or subject not in self.data.columns:
            return None
        if '男' not in self.data['性别'].values or '女' not in self.data['性别'].values:
            return None
        group = self.data.groupby('性别')[subject]
        return {
            '男生平均分': round(group.get_group('男').mean(), 2),
            '女生平均分': round(group.get_group('女').mean(), 2),
            '男生中位数': round(group.get_group('男').median(), 2),
            '女生中位数': round(group.get_group('女').median(), 2)
        }

    def class_performance(self):
        if '班级' not in self.data.columns or '总分' not in self.data.columns:
            return None
        result = self.data.groupby('班级').agg(
            平均总分=('总分', 'mean'),
            最高总分=('总分', 'max'),
            最低总分=('总分', 'min'),
            人数=('学号', 'count')
        ).round(2).reset_index()
        return result

    def score_distribution(self, subject, bins=None):
        if subject not in self.data.columns:
            return None
        if bins is None:
            bins = [0, 60, 70, 80, 90, 101]
            labels = ['不及格', '及格', '中等', '良好', '优秀']
        else:
            labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(len(bins) - 1)]
        return pd.cut(self.data[subject], bins=bins, labels=labels, right=False).value_counts().sort_index()

    def correlation_analysis(self):
        subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
        return self.data[subjects].corr().round(2) if all(col in self.data.columns for col in subjects) else None


# 通用方法
def show_info(title, msg):
    QMessageBox.information(None, title, msg)


def show_warning(title, msg):
    QMessageBox.warning(None, title, msg)


def update_table(table, data):
    table.setRowCount(len(data))
    for row_idx, row in enumerate(data.values):
        for col_idx, value in enumerate(row):
            if isinstance(value, float):
                display = "NaN" if pd.isna(value) else str(int(value)) if value.is_integer() else f"{value:.1f}"
            else:
                display = str(value)
            item = QTableWidgetItem(display)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, col_idx, item)


# 数据展示窗口
class DataViewerTab(QWidget):
    def __init__(self, data_model):
        super().__init__()
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        for btn in [('加载数据', self.load_data), ('保存数据', self.save_data), ('添加学生', self.add_student),
                    ('删除学生', self.remove_student)]:
            b = QPushButton(btn[0])
            b.clicked.connect(btn[1])
            btn_layout.addWidget(b)
        layout.addLayout(btn_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            '学号', '姓名', '性别', '年龄', '班级',
            '语文', '数学', '英语', '物理', '化学', '生物', '总分'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.update_table()

    def load_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开数据文件", "", "CSV文件 (*.csv)")
        if path and self.data_model.load_data(path):
            self.update_table()
            show_info("成功", "数据加载成功！")
        else:
            show_warning("错误", "无法加载数据文件！")

    def save_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存数据文件", "", "CSV文件 (*.csv)")
        if not path:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("选择文件编码")
        layout = QVBoxLayout(dialog)

        combo = QComboBox()
        combo.addItems(["UTF-8 with BOM (推荐)", "UTF-8", "GBK", "GB2312"])
        layout.addWidget(QLabel("请选择文件编码:"))
        layout.addWidget(combo)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(button_box)

        # 设置按钮点击后对话框的行为
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            encodings = {
                "UTF-8 with BOM (推荐)": 'utf_8_sig',
                "UTF-8": 'utf-8',
                "GBK": 'gbk',
                "GB2312": 'gb2312'
            }
            encoding = encodings.get(combo.currentText(), 'utf_8_sig')
            if self.data_model.save_data(path, encoding):
                show_info("成功", f"数据保存成功！(编码: {combo.currentText()})")
            else:
                show_warning("错误", "无法保存数据文件！")

    def add_student(self):
        import random
        names = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]
        classes = ["一班", "二班", "三班", "四班"]
        student = {
            '学号': f"2023{random.randint(1000, 9999)}",
            '姓名': random.choice(names),
            '性别': random.choice(['男', '女']),
            '年龄': random.randint(16, 18),
            '班级': random.choice(classes),
            '语文': random.randint(50, 100),
            '数学': random.randint(50, 100),
            '英语': random.randint(50, 100),
            '物理': random.randint(50, 100),
            '化学': random.randint(50, 100),
            '生物': random.randint(50, 100)
        }
        if self.data_model.add_student(student):
            self.update_table()
            show_info("成功", "学生添加成功！")
        else:
            show_warning("错误", "无法添加学生！")

    def remove_student(self):
        row = self.table.currentRow()
        if row >= 0:
            sid = self.table.item(row, 0).text()
            if self.data_model.remove_student(sid):
                self.update_table()
                show_info("成功", "学生删除成功！")
            else:
                show_warning("错误", "无法删除学生！")
        else:
            show_warning("警告", "请先选择要删除的学生！")

    def update_table(self):
        update_table(self.table, self.data_model.get_data())


# 数据清洗窗口
class DataCleaningTab(QWidget):
    def __init__(self, data_model):
        super().__init__()
        self.data_model = data_model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        control_layout = QHBoxLayout()

        # 缺失值处理
        missing = QGroupBox("缺失值处理")
        mlayout = QVBoxLayout()
        self.missing_combo = QComboBox()
        self.missing_combo.addItems(["删除包含缺失值的行", "用平均值填充", "用中位数填充", "用0填充"])
        self.missing_btn = QPushButton("执行处理")
        self.missing_btn.clicked.connect(self.handle_missing)
        mlayout.addWidget(self.missing_combo)
        mlayout.addWidget(self.missing_btn)
        missing.setLayout(mlayout)

        # 重复值处理
        duplicate = QGroupBox("重复值处理")
        dlayout = QVBoxLayout()
        self.duplicate_btn = QPushButton("删除重复记录")
        self.duplicate_btn.clicked.connect(self.handle_duplicate)
        dlayout.addWidget(self.duplicate_btn)
        duplicate.setLayout(dlayout)

        # 异常值处理
        outlier = QGroupBox("异常值处理")
        olayout = QFormLayout()
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["语文", "数学", "英语", "物理", "化学", "生物", "总分"])
        self.method_combo = QComboBox()
        self.method_combo.addItems(["删除", "用中位数替换", "用平均值替换"])
        self.threshold_edit = QLineEdit("3")
        self.threshold_edit.setToolTip("标准差的倍数，通常2-3之间")
        self.outlier_btn = QPushButton("处理异常值")
        self.outlier_btn.clicked.connect(self.handle_outliers)
        olayout.addRow("科目:", self.subject_combo)
        olayout.addRow("处理方法:", self.method_combo)
        olayout.addRow("阈值(标准差倍数):", self.threshold_edit)
        olayout.addRow(self.outlier_btn)
        outlier.setLayout(olayout)

        control_layout.addWidget(missing)
        control_layout.addWidget(duplicate)
        control_layout.addWidget(outlier)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            '学号', '姓名', '性别', '年龄', '班级',
            '语文', '数学', '英语', '物理', '化学', '生物', '总分'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addLayout(control_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.update_table()

    def update_table(self):
        update_table(self.table, self.data_model.get_data())

    def handle_missing(self):
        data = self.data_model.get_data().copy()
        method = self.missing_combo.currentText()
        if method == "删除包含缺失值的行":
            self.data_model.data = data.dropna()
        else:
            numeric_cols = data.select_dtypes(include=np.number).columns
            fill_value = {'用平均值填充': data[numeric_cols].mean(), '用中位数填充': data[numeric_cols].median(),
                          '用0填充': 0}.get(method)
            data[numeric_cols] = data[numeric_cols].fillna(fill_value)
            self.data_model.data = data
        self.data_model._calculate_total()
        self.update_table()
        show_info("成功", "缺失值处理完成！")

    def handle_duplicate(self):
        data = self.data_model.get_data().copy()
        initial_count = len(data)
        self.data_model.data = data.drop_duplicates()
        final_count = len(self.data_model.get_data())
        self.update_table()
        show_info("成功", f"已删除 {initial_count - final_count} 条重复记录！")

    def handle_outliers(self):
        subject = self.subject_combo.currentText()
        method = self.method_combo.currentText()
        try:
            threshold = float(self.threshold_edit.text())
        except:
            threshold = 3.0
            self.threshold_edit.setText("3.0")
        data = self.data_model.get_data().copy()
        subject_data = data[subject].dropna()
        if len(subject_data) == 0:
            show_warning("错误", f"{subject}列没有有效数据！")
            return
        mean, std = subject_data.mean(), subject_data.std()
        lower, upper = mean - threshold * std, mean + threshold * std
        outliers = (data[subject] < lower) | (data[subject] > upper)
        if method == "删除":
            cleaned = data[~outliers]
        else:
            replace_value = subject_data.median() if method == "用中位数替换" else mean
            cleaned = data.copy()
            cleaned.loc[outliers, subject] = replace_value
        self.data_model.data = cleaned
        self.data_model._calculate_total()
        self.update_table()
        show_info("成功", f"处理了 {outliers.sum()} 个异常值！")


# 数据分析窗口
class DataAnalysisTab(QWidget):
    def __init__(self, data_model):
        super().__init__()
        self.data_model = data_model
        self.analyzer = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        analysis_group = QGroupBox("分析类型")
        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems([
            "单科成绩统计",
            "性别对比分析",
            "班级表现分析",
            "成绩分布分析",
            "学科相关性分析"
        ])
        self.analysis_combo.currentIndexChanged.connect(self.update_parameters)
        analysis_layout = QVBoxLayout()
        analysis_layout.addWidget(self.analysis_combo)
        self.params_group = QGroupBox("分析参数")
        self.params_layout = QVBoxLayout()
        self.params_group.setLayout(self.params_layout)
        analysis_layout.addWidget(self.params_group)
        analysis_group.setLayout(analysis_layout)
        self.analyze_btn = QPushButton("执行分析")
        self.analyze_btn.clicked.connect(self.perform_analysis)
        control_layout.addWidget(analysis_group)
        control_layout.addWidget(self.analyze_btn)
        control_layout.addStretch()
        control_panel.setLayout(control_layout)

        # 结果展示
        result_panel = QWidget()
        result_layout = QVBoxLayout()
        self.result_table = QTableWidget()
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        result_layout.addWidget(self.result_table, 1)
        result_layout.addWidget(self.canvas, 2)
        result_panel.setLayout(result_layout)

        splitter.addWidget(control_panel)
        splitter.addWidget(result_panel)
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        self.update_parameters()

    def update_parameters(self):
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        analysis_type = self.analysis_combo.currentText()
        if analysis_type in ["单科成绩统计", "性别对比分析"]:
            self.subject_combo = QComboBox()
            self.subject_combo.addItems(["语文", "数学", "英语", "物理", "化学", "生物", "总分"])
            self.params_layout.addWidget(QLabel("选择科目:"))
            self.params_layout.addWidget(self.subject_combo)
        elif analysis_type == "成绩分布分析":
            self.subject_combo = QComboBox()
            self.subject_combo.addItems(["语文", "数学", "英语", "物理", "化学", "生物", "总分"])
            self.params_layout.addWidget(QLabel("选择科目:"))
            self.params_layout.addWidget(self.subject_combo)
            self.bins_edit = QLineEdit("0,60,70,80,90,101")
            self.params_layout.addWidget(QLabel("分数段划分:"))
            self.params_layout.addWidget(self.bins_edit)

    def perform_analysis(self):
        if self.data_model.data.empty:
            show_warning("警告", "没有数据可供分析！")
            return
        self.analyzer = DataAnalyzer(self.data_model.get_data())
        analysis_type = self.analysis_combo.currentText()
        try:
            if analysis_type == "单科成绩统计":
                self.show_summary(self.analyzer.subject_summary(self.subject_combo.currentText()), "成绩统计")
            elif analysis_type == "性别对比分析":
                self.show_gender_comparison(self.analyzer.gender_comparison(self.subject_combo.currentText()),
                                            "性别对比")
            elif analysis_type == "班级表现分析":
                self.show_class_performance(self.analyzer.class_performance())
            elif analysis_type == "成绩分布分析":
                try:
                    bins = [int(x) for x in self.bins_edit.text().split(',')]
                except:
                    bins = [0, 60, 70, 80, 90, 101]
                    self.bins_edit.setText("0,60,70,80,90,101")
                self.show_score_distribution(self.analyzer.score_distribution(self.subject_combo.currentText(), bins),
                                             "成绩分布")
            elif analysis_type == "学科相关性分析":
                self.show_correlation(self.analyzer.correlation_analysis())
        except Exception as e:
            show_warning("错误", f"分析过程中发生错误: {str(e)}")

    def show_summary(self, result, title):
        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["指标", "数值"])
        for i, (k, v) in enumerate(result.items()):
            self.result_table.setItem(i, 0, QTableWidgetItem(k))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(v)))
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        labels = list(result.keys())[:4]
        values = [result[k] for k in labels]
        self.ax.bar(labels, values, color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'])
        self.ax.set_title(title)
        self.figure.tight_layout()
        self.canvas.draw()

    def show_gender_comparison(self, result, title):
        self.result_table.setRowCount(2)
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["指标", "男生", "女生"])
        for i, (k, m, f) in enumerate([("平均分", "男生平均分", "女生平均分"), ("中位数", "男生中位数", "女生中位数")]):
            self.result_table.setItem(i, 0, QTableWidgetItem(k))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(result[m])))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(result[f])))
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        labels = ['平均分', '中位数']
        male_values = [result['男生平均分'], result['男生中位数']]
        female_values = [result['女生平均分'], result['女生中位数']]
        x = np.arange(len(labels))
        width = 0.35
        self.ax.bar(x - width / 2, male_values, width, label='男生', color='#4C72B0')
        self.ax.bar(x + width / 2, female_values, width, label='女生', color='#C44E52')
        self.ax.set_title(title)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels)
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

    def show_class_performance(self, result):
        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(len(result.columns))
        self.result_table.setHorizontalHeaderLabels(result.columns)
        for i, row in enumerate(result.values):
            for j, v in enumerate(row):
                self.result_table.setItem(i, j, QTableWidgetItem(str(v)))
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.bar(result['班级'], result['平均总分'], color='#55A868')
        self.ax.set_title("班级平均总分比较")
        self.figure.tight_layout()
        self.canvas.draw()

    def show_score_distribution(self, result, title):
        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["分数段", "人数"])
        for i, (k, v) in enumerate(result.items()):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(v)))
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.pie(result.values, labels=result.index.tolist(), autopct='%1.1f%%',
                    colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#C5A3FF'])
        self.ax.set_title(title)
        self.figure.tight_layout()
        self.canvas.draw()

    def show_correlation(self, result):
        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(len(result))
        self.result_table.setHorizontalHeaderLabels(result.columns.tolist())
        for i, row in enumerate(result.values):
            for j, v in enumerate(row):
                item = QTableWidgetItem(f"{v:.2f}")
                item.setBackground(
                    Qt.GlobalColor.green if v > 0.7 else Qt.GlobalColor.red if v < 0.3 else Qt.GlobalColor.white)
                self.result_table.setItem(i, j, item)
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        cax = self.ax.matshow(result, cmap='coolwarm', vmin=-1, vmax=1)
        self.ax.set_xticks(np.arange(len(result.columns)))
        self.ax.set_yticks(np.arange(len(result.columns)))
        self.ax.set_xticklabels(result.columns)
        self.ax.set_yticklabels(result.columns)
        for i in range(len(result.columns)):
            for j in range(len(result.columns)):
                self.ax.text(j, i, f"{result.iloc[i, j]:.2f}", ha="center", va="center", color="w")
        self.ax.set_title("学科相关性分析")
        self.figure.colorbar(cax)
        self.figure.tight_layout()
        self.canvas.draw()


# 主窗口
class StudentAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("学生成绩数据分析系统")
        self.setGeometry(100, 100, 1200, 800)
        self.data_model = StudentData()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(DataViewerTab(self.data_model), "数据管理")
        self.tabs.addTab(DataCleaningTab(self.data_model), "数据清洗")
        self.tabs.addTab(DataAnalysisTab(self.data_model), "数据分析")
        self.create_menu()
        self.load_sample_data()

    def create_menu(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")
        actions = [
            ("加载数据", self.tabs.widget(0).load_data),
            ("保存数据", self.tabs.widget(0).save_data),
            ("退出", self.close)
        ]
        for name, handler in actions:
            action = QAction(name, self)
            action.triggered.connect(handler)
            file_menu.addAction(action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(
            lambda: show_info("关于", "学生成绩数据分析系统\n版本 1.0\n使用 PyQt6 开发\n© 2025"))
        help_menu.addAction(about_action)

    def load_sample_data(self):
        np.random.seed(42)
        num_students = 100
        names = ["张", "王", "李", "赵", "陈", "刘", "杨", "黄", "周", "吴"]
        full_names = [np.random.choice(names) + np.random.choice(["伟", "芳", "娜", "磊", "洋"]) for _ in
                      range(num_students)]

        # 创建初始 DataFrame
        data = {
            '学号': [f"2023{1000 + i}" for i in range(num_students)],
            '姓名': full_names,
            '性别': np.random.choice(["男", "女"], num_students).tolist(),
            '年龄': np.random.randint(16, 19, num_students).tolist(),
            '班级': np.random.choice(["一班", "二班", "三班", "四班"], num_students).tolist(),
            '语文': np.random.normal(75, 15, num_students).clip(30, 100).tolist(),
            '数学': np.random.normal(70, 20, num_students).clip(30, 100).tolist(),
            '英语': np.random.normal(80, 10, num_students).clip(30, 100).tolist(),
            '物理': np.random.normal(65, 18, num_students).clip(30, 100).tolist(),
            '化学': np.random.normal(72, 16, num_students).clip(30, 100).tolist(),
            '生物': np.random.normal(78, 14, num_students).clip(30, 100).tolist()
        }

        df = pd.DataFrame(data)

        # 添加缺失值
        subject_cols = ['语文', '数学', '英语', '物理', '化学', '生物']
        for col in subject_cols:
            idx = np.random.choice(num_students, 5, replace=False)
            df.loc[idx, col] = np.nan

        # 添加重复记录
        duplicate_idx = np.random.choice(num_students, 5, replace=False)
        duplicates = df.iloc[duplicate_idx].copy()
        df = pd.concat([df, duplicates], ignore_index=True)

        # 计算总分
        df['总分'] = df[subject_cols].sum(axis=1)
        df['年龄'] = df['年龄'].astype(int)

        # 加载到模型
        self.data_model.data = df
        self.tabs.widget(0).update_table()
        self.tabs.widget(1).update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentAnalysisApp()
    window.show()
    sys.exit(app.exec())
