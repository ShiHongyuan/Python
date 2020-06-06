# 最早计算机由美国人发明，编码是ASCII

# 为了显示中文，中国制定了GB2312

# 每个国家去指定一个编码，就可能有冲突，把所有国家都集成在一个编码里，就是Unicode，Unicode是两个字节，但是英文用Unicode就浪费空间
# 可变长编码：UTF-8，1-6个字节，英文用1个字节，中文用3个字节，生僻字用4-6个字节
# 存储和传输用UTF-8，内存里用Unicode，所以过程是，编辑时是Unicode->保存成UTF-8->传输UTF-8->保存UTF-8->打开时转成Unicode到内存里，读取->编辑后再保存转成Unicode存到硬盘里

# 网页的元信息<meta charset="UTF-8"/>表示的是网页传输时的编码，告诉浏览器就以这个编码来解析网页

# Python3是Unicode编码的，所以可以用/u(Unicode编码符号)告诉用Unicode的编码方式来读字符串
print('\u4e2d\u6587')  # 中文
print('\u0000\u0041')  # A （A的编码就是65：01000001，Unicode编码是00000000 01000001）
print('\u0041')  # A （因为前一个字节都是0，所以可以省略）

# 编码和字符的转换
# 字符转编码
print(ord('A'))  # 65
print(ord('中'))  # 20013
# 编码转字符
print(chr(65))  # A
print(chr(20013))  # 中

# 把字符串或者字符转成bytes字符数组
print('ABC'.encode('ascii'))  #  b'ABC' 以ascii编码的字节数组，只要能以单个字节编码显示时就用英文字符
print('ABC'.encode('utf-8'))  # b'ABC' 以utf-8编码的字节数组，只要能以单个字节编码显示时就用英文字符组

print('中文'.encode('utf-8'))  # b'\xe4\xb8\xad\xe6\x96\x87'

# 把获取到的bytes字节流转成字符串或字符
print(b'ABC'.decode('ascii'))  # ABC
print(b'ABC'.decode('utf-8'))  # ABC
print(b'\x41\x42\x43'.decode('utf-8'))  # ABC

print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))  # 中文

# 给bytes数组赋值
stream1 = b'\x41\x42\x43'
print(stream1)  # b'ABC'  只要能以单个字节编码显示时就用英文字符
stream2 = b'\xe4\xb8\xad\xe6\x96\x87'
print(stream2)  # b'\xe4\xb8\xad\xe6\x96\x87'

# 由于Python源代码也是一个文本文件，所以，当你的源代码中包含中文的时候，，我们通常在文件开头写上这两行：
# !/usr/bin/env python3  告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释
# _*_ coding: utf-8      告诉Python解释器，按照UTF-8编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码
# .py文件按utf-8编码保存，perferences -> file encoding -> utf-8 with no BOM


#########################  base64
# 请写一个能处理去掉=的base64解码函数：

# -*- coding: utf-8 -*-
import base64
def safe_base64_decode(s):
    str = s.decode('ascii')
    n = len(str) % 4
    if n != 0:
        for i in range(n):
            str = str + '='
    return base64.b64decode(str.encode('ascii'))


# 或者：
def safe_base64_decode(s):
    n = len(s) % 4
    if n != 0:
        for i in range(n):
            s = s + b'='
    return base64.b64decode(s)


# 测试:
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')







