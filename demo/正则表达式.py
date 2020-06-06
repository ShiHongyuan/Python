############################
# \d匹配一个数字  \w匹配一个字母或者数字    \s 匹配一个空格（也包括Tab等空白符）
# .匹配一个字符
# * 匹配任意个字符（包括0个）   ？匹配0个或1个字符    + 匹配1个或多个字符     {n}匹配n个字符     {n, m}匹配n-m个字符    {0,} 匹配0次以上,逗号后面为空表示无限次的意思
# 匹配特殊字符（除了字母数字外，都是特殊字符），在正则表达式中，要用'\'转义：如'-'要用'\-'，如'_'用'\_'

# [0-9a-zA-Z\_]匹配一个数字、字母或者下划线
# (A|B)可以匹配A或B
# ^表示行的开头，^\d表示必须以数字开头。
# $表示行的结束，\d$表示必须以数字结束。


############################# re模块
import re

# 强烈建议正则表达式使用Python的r前缀，就不用考虑转义的问题了：
# 因为-在正则表达式里是特殊字符，要转义\-，但是正则表达式本身是字符串，-不需要转义，\需要转义，所以用单纯的字符串来表示正则表达式'ABC\-001'必须是s='ABC\\-001'
# 所以还不如否用r前缀来表示正则表达式，如下：
s = r'ABC\-001'
print(re.match(s, 'ABC-001'))  # <re.Match object; span=(0, 7), match='ABC-001'>  匹配成功，返回Match对象

print(re.match(r'^\d{3}\-\d{3,8}$', '010-12345'))  # <re.Match object; span=(0, 9), match='010-12345'>
print(re.match(r'^\d{3}\-\d{3,8}$', '010 12345'))  # None

# match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None：
test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')



################################  用正则表达式切分字符串
l = re.split(r'[\s\,\;]+', 'a,b;; c  d')
print(l)  # ['a', 'b', 'c', 'd']


#############################   从Match对象提取子串
# 通过()匹配的子串对保存在返回的Match对象里
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
# 提取()匹配的子串，如果是大括号里面有小括号，大括号排序在前面，然后是其中的小括号按顺序排序
# 注意：没有匹配到的比如说(...)?没匹配，那么在group()里也要占位，子串是None
print(m.group(0))  # 010-12345
print(m.group(1))  # 010
print(m.group(2))  # 12345
# print(m.group(3))  # 超过分组的个数了，IndexError: no such group
# groups()提取的不包含原始字符串
print(re.match(r'^(\d{3})-(\d{3,8})$', '010-12345').groups())  # ('010', '12345')



############################   贪婪匹配与非贪婪匹配
# 贪婪匹配，也就是匹配尽可能多的字符
# 由于\d+默认采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了。
print(re.match(r'^(\d+)(0*)$', '102300').groups())  # ('102300', '')

# 非贪婪匹配，尽可能少的匹配
# 只需要在需要非贪婪匹配的地方后面加？，就可以转换成非贪婪匹配
# 加个?就可以让\d+采用非贪婪匹配
print(re.match(r'^(\d+?)(0*)$', '102300').groups())  # ('1023', '00')




############################## 预编译正则表达式

# 当我们在Python中使用正则表达式时，re模块内部会干两件事情：
# 编译正则表达式，如果正则表达式的字符串本身不合法，会报错；
# 用编译后的正则表达式去匹配字符串。

# 如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，接下来重复使用时就不需要编译这个步骤了，直接匹配：
# 编译:
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')  # 编译后生成Regular Expression对象，由于该对象自己包含了正则表达式，所以调用对应的方法时不用给出正则字符串
# 使用：
print(re_telephone.match('010-12345').groups())  # ('010', '12345')
print(re_telephone.match('010-8086').groups())  # ('010', '8086')





##################  提取出带名字的Email地址：
# <Tom Paris> tom@voyager.org => Tom Paris
# bob@example.com => bob

# -*- coding: utf-8 -*-
import re
def name_of_email(addr):
    s = r'^\<?(\w+\s*\w+)?\>?(\s*\w+)?(\.\w+)?\@(\w+\.\w+)$'
    print(re.match(s, addr))
    print(re.match(s, addr).groups())
    return re.match(s, addr).groups()[0]
# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')
# 结果：
# <re.Match object; span=(0, 27), match='<Tom Paris> tom@voyager.org'>
# ('Tom Paris', ' tom', None, 'voyager.org')
# <re.Match object; span=(0, 15), match='tom@voyager.org'>
# ('tom', None, None, 'voyager.org')
# ok






