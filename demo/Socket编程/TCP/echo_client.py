import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 客户端也采用ipv4协议和TCP协议
    s.connect(('127.0.0.1', 9999))  # 建立连接
    print(s.recv(1024).decode('utf-8'))  # 接收欢迎语，recv会一直等，直到收到
    for data in [b'Michael', b'Tracy', b'Sarah']:
        s.send(data)  # 因为是字节数组，而且都是英文字符，可以作为传输的字节流，即使按utf-8解码也正确，所以就不需要再编码了
        print(s.recv(1024).decode('utf-8'))  # 接收Hello语句，recv会一直等，直到收到
    s.send(b'exit')
    s.close()


if __name__ == '__main__':
    main()

