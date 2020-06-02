####################### 与、或、非
# and 与
print(True and False)  # False
# or 或
print(True or False)  # True
# not 非
print(not False)  # True


############################  if
height = 1.75
weight = 80.5
bmi = weight / (height * height)
if bmi > 32:
    print('严重肥胖')
elif bmi >= 28 and bmi < 32:
    print('肥胖')
elif bmi >= 25 and bmi < 28:
    print('过重')
elif bmi >= 18.5 and bmi < 25:
    print('正常')
else:
    print('过轻')
# 过重



# 当值本身具有布尔特性时，只需要一个值就可以判断

# x是数值（整数或浮点），零为假，非零为真（非零负数也为真）
x = 0
if x:
    print('True')
else:
    print(False)
# False

x = -1
if x:
    print('True')
else:
    print(False)
# True

x = 0.0
if x:
    print('True')
else:
    print(False)
# False

x = 0.1
if x:
    print('True')
else:
    print(False)
# True

# x是str，空为假，非空为真
x = ''
if x:
    print('True')
else:
    print(False)
# False

x = 'abc'
if x:
    print('True')
else:
    print(False)
# True

# x是list或者tuple，空数组为假，非空为真
x = []
if x:
    print('True')
else:
    print(False)
# False

x = [1]
if x:
    print('True')
else:
    print(False)
# True

x = ()
if x:
    print('True')
else:
    print(False)
# False

x = (1,)
if x:
    print('True')
else:
    print(False)
# True


# x是None，永假
x = None
if x:
    print('True')
else:
    print(False)
# False

# x是布尔值，直接判断
x = True
if x:
    print('True')
else:
    print(False)
# True

# 条件比较，需要两者类型一致
# 输入的都是str类型，str和int比较，要先转换成int
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
# birth: 1992
# 00前



#################################### for in
# list 或者 tuple
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
# Michael
# Bob
# Tracy

sum = 0
p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for x in p:
    sum = sum + x
print(sum)  # 55

# for循环里，同时引用了两个变量
for x, y in [(1, 1), (2, 4), (3, 9)]:
     print(x, y)
# 1 1
# 2 4
# 3 9

# dict
# 取keys
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
# a
# b
# c


# 取values
for value in d.values():
    print(value)
# 1
# 2
# 3


# 取键值对
for k, v in d.items():
    print('%s : %s' % (k, v))
# a : 1
# b : 2
# c : 3



# 字符串str
# 取字符
for ch in 'ABC':
    print(ch)
# A
# B
# C




# enumerate函数可以把一个list变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)
# 0 A
# 1 B
# 2 C



# 判断一个对象是可迭代对象，用collections模块的Iterable类型，Iterable类型表示可迭代类型
from collections import Iterable
print(isinstance('abc', Iterable))  # True
print(isinstance([1,2,3], Iterable))  # True
print(isinstance(123, Iterable))  # False


#################################### while
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)  # 2500

# break
n = 1
while n <= 100:
    if n > 10:  # 当n = 11时，条件满足，执行break语句
        break  # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
#END


# continue
# 只打印奇数
n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0:  # 如果n是偶数，执行continue语句
        continue  # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(n)
print('END')
# 1
# 3
# 5
# 7
# 9
# END
