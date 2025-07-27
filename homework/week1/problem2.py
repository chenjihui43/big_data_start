import random

def estimate_pi(n):
    count = 0
    for _ in range(n):
        x = random.uniform(0, 1)  # 生成[0,1)区间的随机x坐标
        y = random.uniform(0, 1)  # 生成[0,1)区间的随机y坐标
        # 检查点是否在圆内（圆心(0.5,0.5)，半径0.5）
        if (x - 0.5)**2 + (y - 0.5)**2 <= 0.25:
            count += 1
    return 4 * count / n


points_count = int(input("生成随机点个数："))
pi_estimate = estimate_pi(points_count)

print(f"圆周率估计值: {pi_estimate}")