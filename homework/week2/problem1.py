import random

# 数字
char_list = []
for i in range(48, 58):
    char_list.append(chr(i))
# 大写字母
for i in range(65, 91):
    char_list.append(chr(i))
# 小写字母
for i in range(97, 123):
    char_list.append(chr(i))

print(char_list)

password = ""
for i in range(8):
    random_number = random.randint(0, 61)
    password = password + char_list[random_number]

print(password)
