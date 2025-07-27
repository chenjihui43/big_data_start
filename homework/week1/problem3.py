def display_menu():
    """显示菜单选项"""
    border = '*' * 50
    menu_items = [
        "1. 从文件中读取学生历史信息",
        "2. 查询学生已选修的课程和成绩",
        "3. 录入学生选修课程和成绩",
        "4. 打印所有学生的课程和成绩信息",
        "5. 保存所有学生信息至文件",
        "6. 退出"
    ]
    print('\n' + border)
    for item in menu_items:
        print(item)
    print(border + '\n')

def main():
    """主程序逻辑"""
    while True:
        # 显示菜单
        display_menu()

        # 获取用户输入
        choice = input("请输入选择的功能编号：")

        # 处理用户选择
        if choice == '1':
            print("完成……")
        elif choice == '2':
            print("完成……")
        elif choice == '3':
            print("完成……")
        elif choice == '4':
            print("完成……")
        elif choice == '5':
            print("完成……")
        elif choice == '6':
            print("程序已退出")
            break
        else:
            print("无效的选择，请输入1-6之间的数字")

if __name__ == "__main__":
    main()