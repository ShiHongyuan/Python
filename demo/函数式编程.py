# 函数式编程的一个特点就是，允许把函数本身作为参数传入另一个函数，还允许返回一个函数！

################################ 高阶函数
# 变量可以指向函数
f = abs
print(f(-10))  # 10
# 函数名是变量
# abs = 10
# print(abs(-10)) # 报错，int不能被调用

# 一个函数就可以接收另一个函数作为参数，就称作高阶函数
def add(x, y, f):
    return f(x) + f(y)

print(add(-5, 6, abs))   # 11

# map()
# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator（生成器generator）返回
# map后的结果是一个Iterator，如果不强制获取的话，就不会加载结果，所以可以用list()获取计算出的结果。
# 直接给reduce()用的话，reduce会强制获取计算结果，所以，如果已经用list()获取过结果，就不能再给reduce用了，因为已经获取完了。
def f(x):
    return x * x
r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])  # 这里的r只是一个对象，还没有计算出结果
print(list(r))

# reduce()
# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

# 用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456：
from functools import reduce
CHAR_TO_FLOAT = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '.': -1
}
def str2float(s):
    nums = map(lambda ch: CHAR_TO_FLOAT[ch], s)
    point = 0
    def to_float(f, n):
        nonlocal point
        if n == -1:
            point = 1
            return f
        if point == 0:
            return f * 10 + n
        else:
            point = point * 10
            return f + n / point
    return reduce(to_float, nums, 0.0)  # 0.0始终作为nums的第一个元素，参与到reduce里

# lambda函数：lambda ch: CHAR_TO_FLOAT[ch] 等同于：
def fn(ch):
    return CHAR_TO_FLOAT[ch]

# 函数内定义函数

# nonlocal 在函数内引用外部定义的变量，其作用范围是外部

print(str2float('0'))  # 0.0
print(str2float('123.456'))  # 123.456
print(str2float('123.45600'))  # 123.456
print(str2float('0.1234'))  # 0.12340000000000001
print(str2float('.1234'))  # 0.12340000000000001
print(str2float('120.0034'))  # 120.0034


# filter()
# filter接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
# filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()的结果，需要用list()函数获得所有结果并返回list
# 把一个序列中的空字符串删掉：
def not_empty(s):
    return s and s.strip()
print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))

# 筛选出回数
def is_palindrome(n):
    return str(n) == str(n)[::-1]
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))



# sorted()
# 排序对象是list
# 排序数字，按从小到大，排序str，按首字母大小

print(sorted([36, 5, -12, 9, -21]))  # [-21, -12, 5, 9, 36]

# 接收一个key函数来实现自定义的排序，key指定的函数将作用于list的每一个元素上
print(sorted([36, 5, -12, 9, -21], key=abs))  # [5, 9, -12, -21, 36]

# 实现忽略大小写的排序：
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower))  # ['about', 'bob', 'Credit', 'Zoo']

# 要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))  # ['Zoo', 'Credit', 'bob', 'about']

# 自定义排序函数：按照成绩由高到低排序
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_score(t):
    return t[1]
print(sorted(L, key=by_score, reverse=True))  # [('Adam', 92), ('Lisa', 88), ('Bob', 75), ('Bart', 66)]





# 闭包，函数返回函数
# 解释闭包：在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中
# 每次执行闭包函数，引用的外部变量，此时在外部是什么值，就是什么值，是根据执行时确定的，而不是根据定义时确定的。
# 所以，返回闭包时牢记一点：返回函数不要引用外部的任何循环变量，或者后续会发生变化的变量。
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f = lazy_sum(1, 3, 5, 7, 9)
print(f())



# 利用闭包返回一个计数器函数，每次调用它返回递增整数：
# 1. 第一种方法：用生成器生成全自然数
def createCounter():
    def g():
        n = 1
        while True:
            yield n
            n = n + 1
    g = g()
    def counter():
        return next(g)
    return counter
# 2. 第二种方法：用nonlocal变量，
def createCounter():
    n = 0
    def counter():
        nonlocal n
        n = n + 1
        return n
    return counter


# 测试:
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')


# 匿名函数lambda
# 冒号前面的x表示函数参数。匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
# 可以把匿名函数赋值给一个变量，再利用变量来调用该函数
f = lambda x: x * x
print(f(10))  # 100
# 也可以把匿名函数作为返回值返回
def build(x, y):
    return lambda: x * x + y * y
f = build(1,5)
print(f())  # 26


import functools
# 装饰器函数：增强函数功能，比如在函数调用前后增加日志，函数可以是任何函数，增加日志只需配置完成

# 偏函数函数：当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单
# 本来 int(str, base=10)，默认按十进制转换
int2 = functools.partial(int, base=2)
print(int2('101010'))  # 42