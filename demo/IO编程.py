################################### 调用系统接口，操作目录和文件
# 查找当前目录以及子目录下包含某个字符串的所有文件，并输出它们的相对路径
import os
curpath = os.getcwd()
filestr = 'workspace'
file_list = []
def search_file(path, filestr):
    try:
        for file in os.listdir(path):
            this_path = os.path.join(path, file)
            # logging.info(this_path)
            if (os.path.isfile(this_path)):
                if this_path.find(filestr) != -1:
                    filename = os.path.split(this_path)[1]
                    file_list.append(filename)
            else:
                search_file(this_path, filestr)
    except Exception as e:
        pass
    return file_list

# search_file(r'/Users/Tinashy', filestr)
print(file_list)

############################### 序列化

# Python提供了pickle模块来实现序列化

import pickle
# pickle.dumps()方法把任意对象序列化成一个bytes：
d = dict(name='Bob', age=20, score=88)
pickle.dumps(d)
# pickle.dump()直接把对象序列化后写入一个file-like Object：
with open('dump.txt', 'wb') as f:
    pickle.dump(d, f)
# pickle.loads()方法反序列化出对象
# 直接用pickle.load()方法从一个file-like Object中直接反序列化出对象：
with open('dump.txt', 'rb') as f:
    d = pickle.load(f)
print(d)  # {'name': 'Bob', 'age': 20, 'score': 88}



# Python内置的json模块提供了非常完善的Python对象到JSON格式的转换
import json
# 把Python对象变成一个JSON，dumps()方法返回一个str，内容就是标准的JSON。类似的，dump()方法可以直接把JSON写入一个file-like Object
d = dict(name='Bob', age=20, score=88)
print(json.dumps(d))  # '{"name": "Bob", "age": 20, "score": 88}'  是一个字符串
# 要把JSON反序列化为Python对象，用loads()或者对应的load()方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化：
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str))  # {'age': 20, 'score': 88, 'name': 'Bob'}

# 用JSON序列化对象，默认情况下，dumps()方法不知道如何将Student实例变为一个JSON的{}对象。
# 1. 第一种方法：为对象专门写一个转换函数，再把函数传进去作为dumps()的转换参照参数。
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))  # '{"name": "Bob", "age": 20, "score": 88}'

# 2.第二种方法：可以用lambda函数把任意class的实例变为dict，更方便，但是无法像专门的转换函数那样实现定制
# 通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量，除非定义了__slots__的class没有定义__dict__属性
print(json.dumps(s, default=lambda obj: obj.__dict__))

# 把JSON反序列化为一个Student对象实例，loads()方法首先转换出一个dict对象，然后，我们传入的object_hook函数负责把dict转换为Student实例
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))  # <__main__.Student object at 0x10e8f2ad0>
print(json.loads(json_str, object_hook=dict2student).name)  # Bob










