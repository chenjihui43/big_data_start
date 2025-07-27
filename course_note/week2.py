print(3 ** 3)

# import math
# print(math.ceil(10.2))

from math import floor

print(floor(10.2))

print("数值类型的'宽度'说明")

print('''This is a "Joke".''')

print('\n')
print('\\')
print('\t')

print(chr(10004))

print("金牛座的Unicode编码是：" + chr(9801))

# 字符串索引
str = "Python程序语言设计"
print(str[1])

print("abc" * 3)

str2 = "abcabc"
str2.strip("a")
print(str2)

str3 = "hello"
for c in str3:
    print(c)

str4 = "{}:计算机{}的CPU占用率为{}%。".format("2016-12-31", "PYTHON", 10)
print(str4)

x, y, z = 3, 5, 8
str4 = input("请输入长度")
print(str4)

F = 36
C = F * 1.8 + 32
print("转换后的温度是：", C, "F")
print("转换后的温度是{:.2f}F".format(C))
'''
多行注释
'''

for i in range(5):
    print(i, end='')
print()
for i in range(3, 5):
    print(i, end='')
print()

for i in range(0, 10, 2):
    print(i, end='')
print()

for i in range(5, 3):
    print(i, end='')
print()
x = 1, 2, 3
print(x)
t = ('Lucy', ('Math', 90))
print(t)
print(t[1][1])
s = x + t
print(s)

b = list("first")
print(b)
