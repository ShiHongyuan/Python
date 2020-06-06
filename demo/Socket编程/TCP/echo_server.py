import socket, threading, time

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)  # 客户端地址，表明这是与谁的连接
    sock.send(b'Welcome!')  # 连接后服务端先发送欢迎语，因为是字节数组，而且都是英文字符，可以作为传输的字节流，即使按utf-8解码也正确，所以就不需要再编码了
    while True:
        data = sock.recv(1024)  # 循环接收来自客户端的数据，直到客户端传来'exit'，recv会一直等，直到收到
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))  # 修改客户端传来的数据，再返回给客户端
    sock.close()
    print('Connection from %s:%s closed.' % addr)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 服务端用的的ipv4协议和TCP协议
    s.bind(('127.0.0.1', 9999))  # 绑定监听的网卡ip地址和端口
    s.listen(5)  # 开始监听，最多允许同时服务5个连接
    print('Waiting for connection...')

    while True:
        sock, addr = s.accept()  # 不断循环接收新的连接，获取客户端的连接和地址
        t = threading.Thread(target=tcplink, args=(sock, addr))  # 创建一个新的线程来处理新连接
        t.start()


if __name__ == '__main__':
    main()







