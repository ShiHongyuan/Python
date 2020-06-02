###########################  类型转换
# str转int：int()
# 输入的都是str类型，str和int比较，要先转换成int
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
# birth: 1992
# 00前

# 类型转换，如果所给类型无法转化成有意义的指定类型，就会报错，比如不是数值型无法转换成int
# birth = int('a')
# print(birth)

# 如果可以有意义转换，str也可以转成int
print(int('123'))  # 123

# str转float：float()
print(float('12.3'))  # 12.3

# 数值转str：str()
print(str(123))  # 123
print(str(1.23))  # 1.23

# 转布尔：bool()，0和空值为false，非零和非空为true
print(bool(1.0))  # True
print(bool(0))  # False
print(bool(''))  # False


