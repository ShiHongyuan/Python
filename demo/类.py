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




