######################## 整数
######################## 浮点数

# python的整数和浮点数都没有大小限制，浮点数过大时直接显示inf

# 除法
# 1. 精确值除法，商永远是浮点数，即使整除也是浮点数
print(10 / 3)  # 3.3333333333333335
print(9 / 3)  # 3.0

# 2. 地板除法，只保留商的整数部分
print(10 // 3)  # 3
print(9 // 3)  # 3

# 3. 取余除法，只保留商的余数部分
print(10 % 3)  # 1
print(9 % 3)  # 0

######################### 字符串
# 单引号和双引号都ok，常用单引号
print('ok')
print("ok")

# 保留单引号  I'm ok!
print("I'm ok!")

# 单引号和双引号都保留  I'm "ok"
print('I\'m \"ok\"')

# 保留换行
# I'm learning
# Python
print('I\'m learning\nPython')

# 保留转义符字符，两个\\就变成一个普通字符\
# \
# \
print('\\\n\\')

# 制表符\t
# \	\
print('\\\t\\')

# 单行不转义
# \\\n\\
# \\\t\\
print(r'\\\n\\')
print(r'\\\t\\')

# 多行符
# \1
# \2
# \3
print('''\\1
\\2
\\3''')

# 多行不转义
# \\1
# \\2
# \\3
print(r'''\\1
\\2
\\3''')

# 不管是单行还是多行都保留空格
print('    ')

# 字符：是字符串的一部分，只是单个字符，英文字符或者中文字符或者其他国字符，也是''表示
print('A')  # A
print('中')  # 中


# 字符串长度
print(len('ABC'))  # 3
print(len('中文'))  # 2
# 字节长度
print(len('abc'.encode('utf-8')))  # 3 每一个字节一个英文
print(len('中文'.encode('utf-8')))  # 6 每三个字节一个中文

# 用索引读取字符串
str = '   renhaili xiangyu   '
print(str[10])  # i

# 去掉前后空格，因为str是不可变量，生成新对象，原str不变
print(str.strip())  # renhaili xiangyu
print(str)  #    renhaili xiangyu

# str或者char都可以用lower()，upper()，因为str是不可变量，不会修改原值
str = str.strip().upper()
print(str)  # RENHAILI XIANGYU
str = str[0].lower() + str[1:]
print(str)  # rENHAILI XIANGYU

# 字符串反转
print('12345'[::-1])  # 54321


############################# 字符数组
bs = b'ABC'
print(isinstance(bs, bytes))  # True

############################# 布尔值
print(True)  # True
print(False)  # False
print(True and True)  # True
print(True or False)  # True
print(not True)  # False
print(not False)  # True
print(not 1 > 2)  # True
if 1 < 2:
    print('对了呀')

# None 空值，不是零值

############################# 变量可以被赋值不同类型，动态变量
a = 1
print(a)  # 1
a = 'abc'
print(a)  # abc


############################## list
# 赋值
names = ['Michael', 'Bob',  'Tracy']
print(names)  # ['Michael', 'Bob', 'Tracy']

# 长度
print(len(names))  # 3

# 访问索引，越界报错
print(names[0])  # Michael
print(names[1])  # Bob
print(names[2])  # Tracy

# -1是最后一个元素，-2是倒数第2个元素，-3是倒数第3个元素…… ，越界报错
print('names[-1] == names[2] : %s' % names[-1])  # names[-1] == names[2] : Tracy
print('names[-2] == names[1] : %s' % names[-2])  # names[-2] == names[1] : Bob
print('names[-3] == names[0] : %s' % names[-3])  # names[-3] == names[0] : Michael

# 追加元素到末尾，不返回添加元素
print(names.append('Adam'))  # None
print(names)  # ['Michael', 'Bob', 'Tracy', 'Adam']

# 指定位置插入元素，其余元素保存，不返回添加元素
print(names.insert(1, 'Jack'))  # None
print(names)  # ['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']

# 删除末尾元素，返回删除元素
print(names.pop())  # Adam
print(names)  # ['Michael', 'Jack', 'Bob', 'Tracy']

# 删除指定位置元素，返回删除元素
print(names.pop(1))  # Jack
print(names)  # ['Michael', 'Bob', 'Tracy']

# 重新赋值指定位置元素
print(names)  # ['Michael', 'Bob', 'Tracy']
names[1] = 'Sarah'
print(names)  # ['Michael', 'Sarah', 'Tracy']

# list的元素数据类型可以不同
atrributes = ['Apple', 'a', 123, .1, True, (1, 2)]
print(atrributes)  # ['Apple', 'a', 123, 0.1, True, (1, 2)]

# list可以是多维数组
# 二维数组，长度是一维元素个数
grammars = ['mapython', 'java', ['asp', 'php'], 'scheme']
print(grammars[0])  # mapython
print(grammars[2])  # ['asp', 'php']
print(len(grammars))  # 4

# 获取二维元素的方式
print(grammars[2][0])  # asp
print(grammars[2][1])  # php
print(len(grammars[2]))  # 2

# 或者
p = ['asp', 'php']
grammars = ['mapython', 'java', p, 'scheme']
print(p[0])  # asp
print(grammars[2][0])  # asp

# 空数组，长度0
kong = []
print(kong)  # []
print(len(kong))  # 0

# list排序，在原对象上排序
names.sort()
print(names)

###################################  tuple

# 有序类表，一旦初始化，里面的元素的指针不能修改，但是整个tuple的指针可以变
names = ('Michael', 'Bob', 'Tracy')
print(names)  # ('Michael', 'Bob', 'Tracy')


# 报错
# names[0] = 'shihongyuan'

# ok
names = ['Michael', 'Bob',  'Tracy']
print(names)  # ['Michael', 'Bob', 'Tracy']

names = ('Michael', 'Bob', 'Tracy')

# 长度
print(len(names))  # 3

# 访问索引，越界报错，也支持倒数负数索引访问
print(names[0])  # Michael
print(names[1])  # Bob
print(names[2])  # Tracy
print(names[-1])  # Tracy
print(names[-2])  # Bob
print(names[-3])  # Michael

# 空tuple，长度0
kong = ()
print(kong)  # ()
print(len(kong))  # 0

# 只有一个元素的tuple，要加额外逗，打印出来也有逗号
# 传统定义，()是表达式中的小括号，赋值会被认为是单纯的整数1
t = (1)
print(t)  # 1
# 加末尾逗号，是一个只有一个元素为1的tuple
t = (1,)
print(t)  # (1,)
# 一个字符串会被认为是单纯的字符串，所以一个元素的tuple都要加逗号
t = ('Michael')
print(t)  # Michael

t = ('Michael',)
print(t)  # ('Michael',)



# tuple的元素数据类型可以不同
atrributes = ('Apple', 'a', 123, .1, True, (1, 2))
print(atrributes)  # ('Apple', 'a', 123, 0.1, True, (1, 2))

# tuple可以是多维数组
# 二维数组，长度是一维元素个数
grammars = ('mapython', 'java', ['asp', 'php'], 'scheme')
print(grammars[0])  # mapython
print(grammars[2])  # ['asp', 'php']
print(len(grammars))  # 4

# 获取二维元素的方式
print(grammars[2][0])  # asp
print(grammars[2][1])  # php
print(len(grammars[2]))  # 2

# 注意，tuple里包含list，因为list可变，所以tuple里的list可以改变值，只是tuple始终指向这个list不会变
print(grammars)  # ('mapython', 'java', ['asp', 'php'], 'scheme')
grammars[2][0] = 'nodejs'
print(grammars)  # ('mapython', 'java', ['nodejs', 'php'], 'scheme')



###############################  dict

# 初始化赋值 or 后面赋值
d1 = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d2 = {}
d2['Michael'] = 95
d2['Bob'] = 75
d2['Tracy'] = 85
print(d1)  # {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d2)  # {'Michael': 95, 'Bob': 75, 'Tracy': 85}

# 添加key
d1['Jack'] = 90
print(d1)  # {'Michael': 95, 'Bob': 75, 'Tracy': 85, 'Jack': 90}

# 修改value
d1['Jack'] = 88
print(d1)  # {'Michael': 95, 'Bob': 75, 'Tracy': 85, 'Jack': 88}

# 读取key对应的value
# 1. key读取，如果key不存在，dict就会报错
print(d1['Michael'])  # 95
# 2. get()函数读取，如果key不存在，返回None（也可以指定返回默认值，好用于判断）；如果存在，返回对应的value;
print(d1.get('Bob'))  # 75
print(d1.get('hhh'))  # None
print(d1.get('hhh', -1))  # -1

# 判断key存在吗，存在返回True，不存在返回False
print('Bob' in d1)  # True
print('hhh' in d1)  # False

# 删除key，返回删除key对应的value
print(d1.pop('Michael'))  # 95
print(d1)  # {'Bob': 75, 'Tracy': 85, 'Jack': 88}

# key是不可变对象（数值，str，tuple），value可以是不同类型
d1[1] = 1
d1[1.2] = (1, 2, 3)
d1[(1, 2)] = 'str'
print(d1)  # {'Bob': 75, 'Tracy': 85, 'Jack': 88, 1: 1, 1.2: (1, 2, 3), (1, 2): 'str'}

# dict的key必须是不可变对象，在Python中，字符串、整数等都是不可变的，可以放心地作为key。而list是可变的，不能作为key，报错。
# key = [1, 2, 3]
# d1[key] = 'a list key'
# d1[(1, [2, 3])] = 1




############################## set
# 创建一个set，需要提供一个list作为输入集合：
s = set([1, 2, 3])
print(s)  # {1, 2, 3}

# 无序不重复集合，自动过滤重复元素
list = [1, 1, 2, 2, 3, 3]
ss = set(list)
print(ss)  # {1, 2, 3}

# 添加元素
s.add(4)
print(s)  # {1, 2, 3, 4}

# 添加重复元素，不报错，但是添加不上
s.add(4)
print(s)  # {1, 2, 3, 4}

# 两个集合交集
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)  # {2, 3}

# 两个集合并集
print(s1 | s2)  # {1, 2, 3, 4}

# 元素可以是不同类型
s = set(['Apple', 'a', 123, .1, True, (1, 2)])
print(s)  # {0.1, True, (1, 2), 'Apple', 'a', 123}


# set的元素也只能是不可变对象，不能是list
# key = [1, 2, 3]
# s.add(key)
# print(s)
# s.add((1, [2, 3]))
# print(s)



#################################### 常量和枚举
# 定义变量
# 1. 第一种方式：变量名大写，但其实也是变量
# 2. 第二种方式：枚举。
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

# value属性则是自动赋给成员的int常量，默认从1开始计数
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

# Jan => Month.Jan , 1
# Feb => Month.Feb , 2
# Mar => Month.Mar , 3
# Apr => Month.Apr , 4
# May => Month.May , 5
# Jun => Month.Jun , 6
# Jul => Month.Jul , 7
# Aug => Month.Aug , 8
# Sep => Month.Sep , 9
# Oct => Month.Oct , 10
# Nov => Month.Nov , 11
# Dec => Month.Dec , 12

# 如果需要更精确地控制枚举类型，可以从Enum派生出自定义类：
from enum import Enum, unique

# @unique装饰器可以帮助我们检查保证没有重复值：
@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

# 既可以用成员名称引用枚举常量，又可以直接根据value的值获得枚举常量：
day1 = Weekday.Mon
print(day1)  # Weekday.Mon
print(Weekday.Tue)  # Weekday.Tue
print(Weekday['Tue'])  # Weekday.Tue
print(Weekday(1))  # Weekday.Mon
print(Weekday.Tue.value)  # 2
print(day1 == Weekday.Mon)  # True
print(day1 == Weekday.Tue)  # False
print(day1 == Weekday(1))  # True
for name, member in Weekday.__members__.items():
     print(name, '=>', member)
# Sun => Weekday.Sun
# Mon => Weekday.Mon
# Tue => Weekday.Tue
# Wed => Weekday.Wed
# Thu => Weekday.Thu
# Fri => Weekday.Fri
# Sat => Weekday.Sat









