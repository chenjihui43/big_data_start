import random

def guess_number():
    # 生成随机数字（0到10）
    secret_number = random.randint(0, 10)
    attempts = 0
    print("欢迎来到猜数字游戏！数字范围是0到10（整数）。")
    while True:
        try:
            # 获取玩家输入
            guess = int(input("请输入你猜的数字："))
            attempts += 1
            # 判断猜测结果
            if guess < secret_number:
                print("太小了！再试一次。")
            elif guess > secret_number:
                print("太大了！再试一次。")
            else:
                print(f"恭喜！你在第{attempts}次猜对了！")
                break
        except ValueError:
            print("输入无效，请输入0-10的整数！")

# 启动游戏
if __name__ == "__main__":
    guess_number()