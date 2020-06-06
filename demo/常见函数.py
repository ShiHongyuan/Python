############################# range() 生成整数序列

############################# list() 把任意序列转换成list

# range()函数，可以生成一个整数序列，再通过list()函数可以转换为list
# range(5)生成0-4的整数序列，range(101)生成0-100的整数序列
x = list(range(5))
print(x)
# range(2,5)生成2-4的整数序列
print(list(range(2, 5)))  # [2, 3, 4]

############################# set()
# 把数组转换成set
print(set([1, 2, 3]))  # {1, 2, 3}
print(set((1, 2, 3)))  # {1, 2, 3}


#############################  对于可变对象list来说，调用对象自身的任意方法，会改变该对象自身的内容。
names = ['Michael', 'Bob',  'Tracy']
names.sort()
print(names)  # ['Bob', 'Michael', 'Tracy']

d1 = {'Michael': 95, 'Bob': 75, 'Tracy': 85}

############################# 对于不变对象来说，调用对象自身的任意方法，不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回。不可变对象：数值、字符串、tuple都是不可变的
a = 'abc'
b = a.replace('a', 'A')
print(b)
print(a)


############################ 运算函数
# abs(一个数值)
print(abs(12.34))  # 12.34
# max(多个数值)  min(多个数值)
print(max(2, 3, 1, -5))  # 3
print(min(2, 3, 1, -5))  # -5
# 整数转换成十六进制
print(hex(255))  # 0xff


############################ 函数别名
a = abs
print( a(-1) )  # 1


############################# 定义函数
# pass 填充语句块的空函数，什么都不执行
# 如果没有return语句，函数执行完毕后也会返回结果，只是结果为None。return None可以简写为return
def new_function():
    pass
print(new_function())  # None

# 入参做类型检查，不对抛出错误
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    elif x >= 0:
        return x
    else:
        return -x
# print(my_abs('123'))  # TypeError: bad operand type

# 函数可以同时返回多个值，但其实就是一个tuple，但是可以按位置赋给对应的值
# 定义一个函数quadratic(a, b, c)，接收3个参数，返回一元二次方程 ax^2+bx+c=0 的两个解
import math
def quadratic(a, b, c):
    s = math.sqrt(b * b - 4 * a * c)
    x = (-b + s) / (2 * a)
    y = (-b - s) / (2 * a)
    return x, y
x, y = quadratic(2, 3, 1)
print(x, y)  # -0.5 -1.0

########################################## 默认参数，必选参数在前，默认参数在后

# 当不按顺序提供部分默认参数时，需要把参数名写上
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

## 省略了中间的age这个参数，用默认值，但是指定最后的参数city不为默认值
enroll('Adam', 'M', city='Tianjin')
# name: Adam
# gender: M
# age: 6
# city: Tianjin


# 默认参数必须指向不变对象：因为Python函数在定义的时候，默认参数的值就被计算出来了（指针值），如果在函数体中有所修改，指针值不变，内容变了，下次函数再被调用并使用默认值，默认值指针不变，指向的内容每次都会变
def add_end(L=[]):
    L.append('END')
    return L
print(add_end())  # ['END']
print(add_end())  # ['END', 'END']

############################################## 可变参数*，允许传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc(1, 2, 3))  # 14
print(calc())  # 0

# 如果已经有一个list或者tuple，要调用一个可变参数，在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去，传进去的是一份拷贝，不会影响到函数外的nums。
nums = [1, 2, 3]
print(calc(*nums))  # 14

############################################ 关键字参数，允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
print(person('Michael', 30))  # name: Michael age: 30 other: {}
print(person('Jack', 24, city='Beijing', job='Engineer'))  # name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}

# 如果已经有一个dict，要调用关键字参数，在dict前面加一个**，传进去的extra是一份拷贝，不会影响到函数外的extra
extra = {'city': 'Beijing', 'job': 'Engineer'}
print(person('Jack', 24, **extra))  # name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}



######################################### 命名关键字参数，指定只接收并必须接收某些关键字参数，*后面的参数被视为命名关键字参数
# 只接收格外的city和job参数，*用来区分必须参数和命名关键词参数
def person(name, age, *, city, job):
    print(name, age, city, job)
print(person('Jack', 24, city='Beijing', job='Engineer'))  # Jack 24 Beijing Engineer

# 命名关键词参数 + 默认参数
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job)
print(person('Jack', 24, job='Engineer'))  # Jack 24 Beijing Engineer

################################  参数组合：参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
print(f1(1, 2, 3, 'a', 'b', x=99))  # a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}

args = (1, 2, 3, 4)
kw = {'d': 99, 'x': '#'}
print(f1(*args, **kw))  # a = 1 b = 2 c = 3 args = (4,) kw = {'d': 99, 'x': '#'}



################################ 索引切片函数
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
# 从索引0开始取，直到索引3为止，但不包括索引3
print(L[0:3])  # ['Michael', 'Sarah', 'Tracy']
# 如果第一个索引是0，还可以省略
print(L[:3])  # ['Michael', 'Sarah', 'Tracy']
# 如果最后一个索引是尾巴，可以省略，并且大于len(s)的任何数都表示截到最后
print(L[1:])  # ['Sarah', 'Tracy', 'Bob', 'Jack']
print(L[1:5])  # ['Sarah', 'Tracy', 'Bob', 'Jack']
# 也支持负数取倒数的切片，并且最后一个索引是-1.可以省略
print(L[-3:-1])  # ['Tracy', 'Bob']
print(L[-3:])  # ['Tracy', 'Bob', 'Jack']
# 相当于原样复制
print(L[:])  # ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[0:5])  # ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
# 第二个冒号表示每隔多少个取一个
L = list(range(11))
print(L)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 每2个取一个
print(L[::2])  # [0, 2, 4, 6, 8, 10]

# tuple一样
print((0, 1, 2, 3, 4, 5)[:3])  # (0, 1, 2)

# str一样
print('ABCDEFG'[0:6:2])  # ACE



################################# 列表生成式
# 一句话生成列表，for前面是生成式，for后面是生成来源
L = [x * x for x in range(1, 11)]
print(L)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# for后面 + if，筛选部分来源生成，不能有else，因为默认不在if里的就是丢弃
# 只要偶数
L = [x * x for x in range(1, 11) if x % 2 == 0]
print(L)  # [4, 16, 36, 64, 100]

# for前面 + if，生成式的方式不一样，必须有else，要么满足if条件按if生成，要么按else生成
# 偶数生成正数，奇数变负数
L = [x if x % 2 == 0 else -x for x in range(1, 11)]
print(L)  # [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

# 两层及多层循环生成
# 两层笛卡尔积，生成式的+表示合并字符串
L = [m + n for m in 'ABC' for n in 'XYZ']
print(L)  # ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

# 使用两个变量来生成
d = {'x': 'A', 'y': 'B', 'z': 'C'}
L = [k + '=' + v for k, v in d.items()]
print(L)  # ['x=A', 'y=B', 'z=C']

# 只筛选出字符串变小写，生成新的列表
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]
print(L2)  # ['hello', 'world', 'apple']


######################################## 生成器，跟生成式的区别是：需要的时候才生成，一边循环一边计算一边生成
# 1. 定义生成器的第一种方式，用()
g = (x * x for x in range(10))

# 需要的时候，获取下一个值，直到最后抛出StopIteration错误结束，无法继续返回下一个值了
print(next(g))  # 0
print(next(g))  # 1
print(next(g))  # 4

# 一般通过for循环来获取值，for的实质是不断调用next(g)来获取还未生成过的值，for会自动判断到哪里结束，不用自己处理异常
# 注意，生成器是前面生成过的数就不会再生成了
for n in g:
     print(n)
# 9
# 16
# 25
# 36
# 49
# 64
# 81

# 还有一种通过while循环获取，但是不知道有多长，所以要自己捕获异常来终止
while True:
    try:
        x = next(g)
        print('g:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break
# Generator return value: None  前面把数字都生成完了，到最后只有一个默认的异常，异常没有带return的说明



# 2. 定义生成器的第二种方式，用函数+yield的方式：
# yield是生成器的实质，在函数中，每遇到yeild，就生成一个值，停止，下次next(g)，再从yeild开始。
# 直到函数结束，或者return，生成器抛出StopIteration错误结束，无法继续返回下一个值了
# 如果函数的return有返回值，StopIteration的value就是返回值
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(2)
    print('step 3')
    yield(3)
    return 'Done'

# generator函数的“调用”实际返回一个generator对象：
o = odd()
while True:
    try:
        x = next(o)
        print('o:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break
# step 1
# o: 1
# step 2
# o: 2
# step 3
# o: 3
# Generator return value: Done



# 自己做出来的，开心一下：
#           1
#          / \
#         1   1
#        / \ / \
#       1   2   1
#      / \ / \ / \
#     1   3   3   1
#    / \ / \ / \ / \
#   1   4   6   4   1
#  / \ / \ / \ / \ / \
# 1   5   10  10  5   1
# 杨辉三角，把每一行看做一个list，试写一个generator，不断输出下一行的list：
# 期待输出:
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# [1, 4, 6, 4, 1]
# [1, 5, 10, 10, 5, 1]
# [1, 6, 15, 20, 15, 6, 1]
# [1, 7, 21, 35, 35, 21, 7, 1]
# [1, 8, 28, 56, 70, 56, 28, 8, 1]
# [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]

def triangles():
    n = 0
    result = [1]
    while n < 10:
        yield result
        tmp = []
        tmp.append(1)
        l = 0
        while l < len(result) and (l + 1) < len(result):
            tmp.append(result[l] + result[l + 1])
            l = l + 1
        tmp.append(1)
        result = tmp
        n = n + 1
    return


triangles = triangles()
while True:
    try:
        x = next(triangles)
        print('triangles:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break

# triangles: [1]
# triangles: [1, 1]
# triangles: [1, 2, 1]
# triangles: [1, 3, 3, 1]
# triangles: [1, 4, 6, 4, 1]
# triangles: [1, 5, 10, 10, 5, 1]
# triangles: [1, 6, 15, 20, 15, 6, 1]
# triangles: [1, 7, 21, 35, 35, 21, 7, 1]
# triangles: [1, 8, 28, 56, 70, 56, 28, 8, 1]
# triangles: [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
# Generator return value: None


######################################### 迭代器 Iterable

# 可迭代的类型Iterable，可以用for-in循环
# 可迭代对象：list、tuple、str、dict、set、generator
from collections.abc import Iterable
print(isinstance([], Iterable))  # True
print(isinstance((), Iterable))  # True
print(isinstance('abc', Iterable))  # True
print(isinstance({}, Iterable))  # True
print(isinstance(set([]), Iterable))  # True
print(isinstance((x for x in range(10)), Iterable))  # True

# 可迭代对象Iterator，可以用next()获取下一个值
# Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误，不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算
# 只有generator是Iterator对象，其他都是可迭代的类型Iterable，但不是可迭代对象Iterator
# 把list、dict、str等Iterable变成Iterator可以使用iter()函数：
from collections.abc import Iterator
print(isinstance(iter([]), Iterator))  # True
print(isinstance(iter('abc'), Iterator))  # True


###############################  math
import math
# sum([1, 2, 3])
# pow(-1, x//2)
