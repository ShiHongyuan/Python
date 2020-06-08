# 引入了包以后，只要顶层的包名不与别人冲突，那所有模块都不会与别人冲突。现在，abc.py的模块名就变成了mycompany.abc，类似的，xyz.py的模块名变成了mycompany.xyz。
#
# 请注意，每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包。__
# init__.py可以是空文件，也可以有Python代码，因为__init__.py本身就是一个模块，而它的模块名就是mycompany。

############################################## 模块文件范本

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '  # 一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释

__author__ = 'Michael Liao'  # 使用__author__变量把作者写进去，这样当你公开源代码后别人就可以瞻仰你的大名

import sys  # python内建的sys模块

def test():
    # sys模块有一个argv变量，用list存储了命令行的所有参数。argv至少有一个元素，因为第一个参数永远是该.py文件的名称
    # 运行python3 hello.py获得的sys.argv就是['hello.py']；
    # 运行python3 hello.py Michael获得的sys.argv就是['hello.py', 'Michael]。
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')
print('第二个')
test()
# 我们用命令行运行hello.py时，Python解释器把一个特殊变量__name__置为__main__，直接执行test()
# $ python3 hello.py
# Hello, world!
# $ python hello.py Michael
# Hello, Michael!

# 而如果在其他地方导入该hello模块时，if判断将失败。比如在命令行导入时，没有打印Hello, word!，因为没有执行test()函数。调用hello.test()时，才能打印出Hello, word!
# $ python3
# Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 23 2015, 02:52:03)
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import hello
# >>>
# >>> hello.test()
# Hello, world!
if __name__=='__main__':
    print('第一个')
    test()

# 先执行第二个，再执行第一个，按顺序，if是最后判断的


######################################## 变量
# 1. 特殊变量
# 类似__xxx__这样的变量是特殊变量，可以被直接引用，但是有特殊用途，比如上面的__author__，__name__就是特殊变量，hello模块定义的文档注释也可以用特殊变量__doc__访问。
# 我们自己的变量一般不要用这种变量名。

# 2. private
# 类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等。
# 之所以我们说，private函数和变量“不应该”被直接引用，而不是“不能”被直接引用，是因为Python并没有一种方法可以完全限制访问private函数或变量，但是，从编程习惯上不应该引用private函数或变量。
# 外部不需要引用的函数全部定义成private，只有外部需要引用的函数才定义为public。

# 模块里公开greeting()函数，而把内部逻辑用private函数隐藏起来了，这也是一种非常有用的代码封装和抽象的方法。
def _private_1(name):
    return 'Hello, %s' % name


def _private_2(name):
    return 'Hi, %s' % name


def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)


######################################## 安装第三方库
# 第三方库都会在Python官方的pypi.python.org网站注册，要安装一个第三方库，必须先知道该库的名称，可以在官网或者pypi上搜索。
# 比如Pillow的名称叫Pillow，因此，安装Pillow的命令就是：pip install Pillow


######################################## import 搜索路径
# 默认情况下，Python解释器会搜索当前目录、所有已安装的内置模块和第三方模块，搜索路径存放在sys模块的path变量中：
#>>> import sys
# >>> sys.path
# ['', '/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/lib/python37.zip', '/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/lib/python3.7', '/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload', '/usr/local/lib/python3.7/site-packages']

# 如果我们要添加自己的搜索目录，有两种方法：
# 1. 直接修改sys.path，添加要搜索的目录，这种方法是在运行时修改，运行结束后失效：
# >>> import sys
# >>> sys.path.append('Users/Tinashy')

# 2. 设置环境变量PYTHONPATH，该环境变量的内容会被自动添加到模块搜索路径中，设置方式与设置Path环境变量类似。设置时只添加你自己的搜索路径，Python自己本身的搜索路径改变。