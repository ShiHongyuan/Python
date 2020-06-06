##################################### 定义类

# 和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数。


# (object)，表示该类是从哪个类继承下来的，通常，如果没有合适的继承类，就使用object类，这是所有类最终都会继承的类。

# 注意到__init__方法的第一个参数永远是self，表示创建的实例本身，就可以把各种属性绑定到self。
# 创建实例时不能传入空的参数，必须传入与__init__方法匹配的参数，但self不需要传，Python解释器自己会把实例变量传进去。
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))



# 和静态语言不同，Python允许对已存在的实例变量任何绑定其他数据，也就是说，对于两个实例变量，虽然它们都是同一个类的不同实例，但拥有的变量名称都可能不同：
bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.age = 18
print(bart.name, bart.age)  # Bart Simpson 18
# print(lisa.name, lisa.age)  # age属性是后面增加到bart实例的，lisa实例没有这个属性

# 如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，就变成了一个私有变量（private）
# 变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量，所以，不能用__name__、__score__这样的变量名。
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')


bart = Student('Bart Simpson', 60)
# print(bart.__name)  # 'Student' object has no attribute '__name'


# 以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。


# 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量：
# 这个版本就不行，实例没有_Student这个变量
# print(bart._Student.__name)


# 如果已经设置为的私有变量，被实例在外部访问修改，其实能直接访问并修改的不是私有变量，而是给该实例新增的一个外部变量，只是变量名相同：
# 所以，同一个实例，不同的访问类型的变量名可以相同
print(bart.get_name())  # Bart Simpson
bart.__name = 'shihongyuan'
print(bart.__name)  # shihongyuan  能直接访问的是外部的变量__name
print(bart.get_name())  # Bart Simpson  内部的变量__name并没有被修改


# 例子
# 把下面的Student对象的gender字段对外隐藏起来，用get_gender()和set_gender()代替，并检查参数有效性：
class Student(object):
    def __init__(self, name, gender):
        self.__name = name
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        if gender == 'male' or gender == 'female':
            self.__gender = gender
        else:
            raise ValueError('bad gender')



####################################  继承和多态

# 实例不是同一个引用
class Animal(object):
    def run(self):
        print('Animal is running...')

a1 = Animal()
a2 = Animal()
print(a1 == a2)  # False

# 继承可以把父类的所有功能都直接拿过来，这样就不必重零做起，子类只需要新增自己特有的方法，也可以把父类不适合的方法覆盖重写。
class Dog(Animal):
    def run(self):
        print('Dog is running...')

    def eat(self):
        print('Dog is eating...')


class Cat(Animal):
    def run(self):
        print('Cat is running...')

# 在继承关系中，如果一个实例的数据类型是某个子类，那它的数据类型也可以被看做是父类。但是，反过来就不行：
a = Animal()
dog = Dog()
print(isinstance(dog, Animal))  # True
print(isinstance(a, Dog))  # False

# 类继承的使用
def run_twice(animal):
    animal.run()
    animal.run()

run_twice(a)  # Animal is running...  Animal is running...
run_twice(dog)  # Dog is running...  Dog is running...

# 这就是动态语言的“鸭子类型”：由于Python这种动态语言没有变量的数据类型限制，run_twice这种方法不一定需要传入Animal类型，我们只需要保证传入的对象有一个run()方法就可以了
# 它并不要求严格的继承体系，对真正的文件对象，它有一个read()方法，返回其内容。但是，许多对象，只要有read()方法，都被视为“file-like object“。许多函数接收的参数就是“file-like object“，你不一定要传入真正的文件对象，完全可以传入任何实现了read()方法的对象。
class Timer(object):
    def run(self):
        print('Timer Start...')

timer = Timer()
run_twice(timer)  # Timer Start...  Timer Start...

############################# 对象信息

# 对象类型

# 1. type()

# 可以直接得到类型，类名
print(type(1))  # <class 'int'>
print(type('abc'))  # <class 'str'>
print(type(None))  # <class 'NoneType'>
print(type(dog))  # <class '__main__.Dog'>

# 是否是基本类型
print(type(1) == int)  # True
print(type('abc') == str)  # True

# 是否是函数，types模块中有定义常量
import types
def fn():
    pass
print(type(fn) == types.FunctionType)  # True
print(type(abs) == types.BuiltinFunctionType)  # True
print(type(lambda x:x) == types.LambdaType)  # True
print(type((x for x in range(10))) == types.GeneratorType)  # True

# 比较两者类型是否一致
print(type(1) == type(1.2))  # False
print(type(1.2) == type(2.2))  # True
print(type('a') == type('abc'))  # True

# 2. isinstance()  检查类型优先使用isinstance()，可以将指定类型及其子类“一网打尽”。
# 是否是基本类型
print(isinstance('a', str))  # True
print(isinstance(123, int))  # True
print(isinstance(1.2, float))  # True
print(isinstance(b'a', bytes))  # True

# 是否是对象类型
print(isinstance([1, 2, 3], list))  # True
print(isinstance({'a': 1, 'b': 2}, dict))  # True

# 还可以判断一个变量是否是某些类型中的一种：
print(isinstance([1, 2, 3], (list, tuple)))  # True
print(isinstance((1, 2, 3), (list, tuple)))  # True


# 获取对象的属性和方法
# 获取一个对象的所有属性，包括变量和方法
print(dir(dog))
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'eat', 'run']
print(dir('abc'))
# ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

# 类似__xxx__的属性和方法在Python中都是有特殊用途的（有点像object的抽象方法，需要子类自己去具体实现才能用），比如__len__方法返回长度。
# 在Python中，如果你调用len()函数试图获取一个对象的长度，实际上，在len()函数内部，它自动去调用该对象的__len__()方法
print(len('abc'))  # 3
print('abc'.__len__())  # 3

# 我们自己写的类，如果也想用len(myObj)的话，就自己写一个__len__()方法：
class MyDog(object):
    pass
    def __len__(self):
        return 100

myDog = MyDog()
print(len(myDog))  # 100

# getattr()、setattr()、hasattr()
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

aliy = Student('Bart Simpson', 60)
# print(getattr(aliy, '__score'))  私有属性不能访问，认为不存在
print(getattr(aliy, 'get_score'))  # <bound method Student.get_score of <__main__.Student object at 0x107ea4210>>
print(hasattr(aliy, 'grade'))  # False
setattr(aliy, 'grade', 1)
print(hasattr(aliy, 'grade'))  # True
print(aliy.grade)  # 1

# 如果试图获取不存在的属性，会抛出AttributeError的错误：
# getattr(aliy, 'class')  # 'Student' object has no attribute 'class'
# 可以使用default参数，如果属性不存在，就返回默认值：
print(getattr(aliy, 'class', 'math'))  # math



########################################## 类属性：类拥有的属性，实例都一样的属性
# 定义类属性
class Student(object):
    name = 'Student'

s = Student()
print(s.name)  # Student  因为实例并没有name属性，所以会继续查找class的name属性
print(Student.name)  # Student

s.name = 'Michael'
print(s.name)  # Michael  实例属性优先于类属性，因此，它会屏蔽掉类的name属性
print(Student.name)  # Student

del s.name
print(s.name)  # Student



##################################### property
# 利用@property给一个Screen对象加上可读写width和height属性，以及一个只读属性resolution
class Screen(object):

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def resolution(self):
        return self.__width * self.__height
# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')



#################################  动态化处理属性和方法
# __len__() -> len()
# __str__() -> print实例时，自动调用的字符串
# __repr__() -> 直接显示实例时，自动调用的字符串
# __iter__() -> 返回迭代对象，通常是实例自身
# __next__() -> for in实例，自动调用上面的__iter__()，返回迭代对象，并通过迭代对象的__next__()方法循环取值
# __getitem__() -> 让实例能像list那样按照下标取出元素，__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice
# __getattr__() -> 当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，只有在没有找到属性的情况下，才调用__getattr__，已有的属性，比如name，不会在__getattr__中查找。
# __call__() -> 定义后可以把实例变成一个可被调用的Callable对象，当做函数直接调用，就执行__call__()方法
# 判断一个对象是否能被调用，通过callable()函数，我们就可以判断一个对象是否是“可调用”对象
print(callable(max))  # True
print(callable(abs))  # True
print(callable([1, 2, 3]))  # False
print(callable(None))  # False
print(callable('str'))  # False



####################################### 测试类
# 被测试类
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def get_grade(self):
        if not isinstance(self.score, int):
            raise ValueError('bad score')
        if self.score < 0 or self.score > 100:
            raise ValueError('bad score')
        if self.score >= 80:
            return 'A'
        if self.score >= 60:
            return 'B'
        return 'C'

 # 测试类
 # 单元测试的测试用例要覆盖常用的输入组合、边界条件和异常。
 # 单元测试代码要非常简单，如果测试代码太复杂，那么测试代码本身就可能有bug，对每一类的测试都需要编写一个test_xxx()方法。
import unittest
class TestStudent(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test_80_to_100(self):
        s1 = Student('Bart', 80)
        s2 = Student('Lisa', 100)
        self.assertEqual(s1.get_grade(), 'A')
        self.assertEqual(s2.get_grade(), 'A')

    def test_60_to_80(self):
        s1 = Student('Bart', 60)
        s2 = Student('Lisa', 79)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')

    def test_0_to_60(self):
        s1 = Student('Bart', 0)
        s2 = Student('Lisa', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')

    def test_invalid(self):
        s1 = Student('Bart', -1)
        s2 = Student('Lisa', 101)
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(ValueError):
            s2.get_grade()

# if __name__ == '__main__':
#     unittest.main()

# setUp()和tearDown()方法。这两个方法会分别在每调用一个测试方法的前后分别被执行，比如说你的测试需要启动一个数据库，可以在setUp()方法中连接数据库，在tearDown()方法中关闭数据库
class TestDict(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')



######################################### 日志
# logging的另一个好处是通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件。
# 有debug，info，warning，exception，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了。同理，指定level=WARNING后，debug和info就不起作用了。
# 这样一来，你可以放心地输出不同级别的信息，也不用删除，最后统一控制输出哪个级别的信息。
import logging
logging.basicConfig(level=logging.INFO)
s = '0'
try:
    n = int(s)
    print(10 / n)
except Exception as e:
    logging.info('n = %d' % n)
    logging.exception(e)













