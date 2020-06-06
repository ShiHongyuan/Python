import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # 服务端用的的ipv4协议和UDP协议
    s.bind(('127.0.0.1', 9999))  # 绑定监听的网卡ip地址和端口，因为udp不建立连接通道，就没有最大连接数的限制，来就处理，来多少就处理多少，打不了排队处理完了再发
    print('Bind UDP on 9999...')

    while True:
        data, addr = s.recvfrom(1024)  # 不断循环接收客户端发的新的数据和客户端地址，recvfrom没有收到不会等着，而是跳过
        print('Received from %s:%s.' % addr)
        s.sendto(b'Hello, %s!' % data, addr)  # 直接调用sendto()就可以把数据用UDP发给客户端


if __name__ == '__main__':
    main()