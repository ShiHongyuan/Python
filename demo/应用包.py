# 收发邮件，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件：
#                   smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件
#                   Python内置一个poplib模块，实现了POP3协议，可以直接用来收邮件
# 生成二维码图片：Pillow
# 访问网络：urllib、requests（更多高级功能）
# 解析HTML：HTMLParser
# 密码加密：hashlib、hmac
# 生成永久迭代对象：itertools
# 拦截，在执行前后插入其他操作，日志：contextlib
# 其他类型和字节数组b''的转换：struct
# 集合类：collections
# 时间，时区：datetime
# 文本编辑器显示某些二进制，用编码读会显示乱码，为了都正常显示，编码成只有ascii字符的base64编码：base64
# 运维监控，cpu、内存、网络、进程、磁盘：psutil
# 每个应用可能需要各自拥有一套“独立”的Python运行环境。virtualenv就是用来为一个应用创建一套“隔离”的Python运行环境
# 检测编码，便于字节数组通过decode解码成str：chardet
import chardet
chardet.detect(b'Hello, world!')  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}

data = '离离原上草，一岁一枯荣'.encode('gbk')
chardet.detect(data)  # {'encoding': 'GB2312', 'confidence': 0.7407407407407407, 'language': 'Chinese'}

data = '离离原上草，一岁一枯荣'.encode('utf-8')
chardet.detect(data)  # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

# 日文
data = '最新の主要ニュース'.encode('euc-jp')
chardet.detect(data)  # {'encoding': 'EUC-JP', 'confidence': 0.99, 'language': 'Japanese'}
str = data.decode('euc-jp')
print(str)  # 最新の主要ニュース


# 异步IO情况下，用协程：asyncio

# 在Web服务器上，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持：aiohttp