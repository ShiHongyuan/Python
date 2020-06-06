import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 客户端用的的ipv4协议和UDP协议
    for data in [b'Michael', b'Tracy', b'Sarah']:
        s.sendto(data, ('127.0.0.1', 9999))  # 发送数据
        print(s.recv(1024).decode('utf-8'))  # 接收数据，recv会一直等着，收到为止
    s.close()


if __name__ == '__main__':
    main()