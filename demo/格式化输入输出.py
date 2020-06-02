#################################### 格式化输出
# 1. 用%
# %d	整数
# %f	浮点数
# %s	字符串
# %x	十六进制整数

# 如果只有一个占位符%?，括号可以省略
print( 'hello, %s' % 'shihonyuan' )  # hello, shihonyuan
print( 'hello, %s, you have $ %d' % ('Michael', 50) )  # hello, Michael, you have $ 50

# %s 可以把任何类型的参数转换成字符串，永远不会报错的转换
print( 'you have $ %s, Right? %s ' % (50, True))  # you have $ 50, Right? True

# 指定整数或者浮点数的整数部分位数
# 不足不补0： %2d  %2.1f
# 不足补0： %02d  %02.1f

# 指定浮点数的小数部分位数：%.1f  %2.1f
print('%02d' % 3)  # 03
print('%2.1f' % 33.11)  # 33.1



# 2. 用format()，{0}、{1}……表示占位符
print( 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125) )  # Hello, 小明, 成绩提升了 17.1%


#################################### 命令行输入
# input
# 输入的都是str类型，如果要和数值比较，要类型转换成数值
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
# birth: 1992
# 00前

############################ 输出可以是打印多个，模拟字符串
d = {'a': 1, 'b': 2, 'c': 3}
for k, v in d.items():
    print('%s : %s' % (k, v))
# a : 1
# b : 2
# c : 3

# 相当于
for k, v in d.items():
    print(k, ':', v)
# a : 1
# b : 2
# c : 3
