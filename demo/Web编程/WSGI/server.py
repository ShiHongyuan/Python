from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application, application_hasparam

def init():
    httpd = make_server('', 8000, application)  # 创建一个服务器，IP地址为空，端口是8000，处理函数是application
    print('Serving HTTP on port 8000...')

    httpd.serve_forever()  # 开始监听HTTP请求

def init_hasparam():
    httpd = make_server('', 8000, application_hasparam)  # 创建一个服务器，IP地址为空，端口是8000，处理函数是application
    print('Serving HTTP on port 8000...')

    httpd.serve_forever()  # 开始监听HTTP请求


if __name__ == '__main__':
    # init()  # http://localhost:8000
    init_hasparam()  # http://localhost:8000/Michael


