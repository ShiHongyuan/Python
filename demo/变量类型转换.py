###########################  类型转换
# str转int：int()
# 输入的都是str类型，str和int比较，要先转换成int
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
# birth: 1992
# 00前

# 类型转换，如果所给类型无法转化成有意义的指定类型，就会报错，比如不是数值型无法转换成int
# birth = int('a')
# print(birth)

# 如果可以有意义转换，str也可以转成int
print(int('123'))  # 123

# str转float：float()
print(float('12.3'))  # 12.3

# 数值转str：str()
print(str(123))  # 123
print(str(1.23))  # 1.23

# 转布尔：bool()，0和空值为false，非零和非空为true
print(bool(1.0))  # True
print(bool(0))  # False
print(bool(''))  # False

############################ 其他类型和字符数组（bytes）的转换
import struct
# int转bytes
struct.pack('>I', 10240099)  # b'\x00\x9c@c' pack的第一个参数是处理指令，'>I'的意思是：>表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。
# bytes转int
struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')  # (4042322160, 32896)  >IH说明：后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数。

# str与bytes：encode、decode


############################### 编码与字符
# 随机int转字符
import random
chr(random.randint(65, 90))

# 字符转int
ord('a')