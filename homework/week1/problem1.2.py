def string_processing():
    # 获取字符串数量
    while True:
        try:
            n = int(input("请输入字符串数量："))
            if n <= 0:
                print("请输入正整数！")
                continue
            break
        except ValueError:
            print("输入无效，请输入整数！")

    strings = []
    # 获取所有字符串
    for i in range(n):
        s = input(f"请输入第 {i + 1} 个字符串：")
        strings.append(s)

    print("\n处理结果：")
    # 处理每个字符串
    for i, s in enumerate(strings):
        # 初始化计数器
        letters = 0
        digits = 0
        spaces = 0
        others = 0

        # 统计各类字符
        for char in s:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            elif char.isspace():
                spaces += 1
            else:
                others += 1

        # 替换操作
        if "ces" in s:
            modified = s.replace("ces", "cse")
            print(f"\n字符串 {i + 1}: '{s}' 包含'ces'，已替换为: '{modified}'")
        else:
            modified = s
            print(f"\n字符串 {i + 1}: '{modified}'")

        # 输出统计结果
        print(f"字符统计: 字母={letters}, 数字={digits}, 空格={spaces}, 其他={others}")


# 启动程序
if __name__ == "__main__":
    string_processing()