#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'


'''
在开发阶段，让服务器检测到代码修改后自动重新加载模块，把当前进程杀掉，再自动重启服务器进程
只要一保存代码，就可以刷新浏览器看到效果，大大提升了开发效率
'''


import os, sys, time, subprocess
'''
Python的第三方库watchdog可以利用操作系统的API来监控目录文件的变化，并发送通知
'''
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):
    '''
    自定义一个监控文件的类，继承自watchdog的FileSystemEventHandler
    利用watchdog接收文件变化的通知，当文件发生改变时，触发FileSystemEventHandler的处理函数，重写处理函数，如果是.py文件，就自动重启服务器进程
    '''

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    # 重写处理函数，如果是.py文件，就自动重启服务器进程
    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

command = ['echo', 'ok']
process = None

def kill_process():
    '''
    杀掉进程，全部变量process
    :return:
    '''
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None

def start_process():
    '''
    启动进程，给全局变量process
    :return:
    '''
    global process, command
    log('Start process %s...' % ' '.join(command))
    # 启动进程执行命令为：command=python3 app.py
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def restart_process():
    '''
    重启进程，更新全局变量process
    :return:
    '''
    kill_process()
    start_process()

def start_watch(path, callback):
    '''
    启动watchdog的监控
    :param path:
    :param callback:
    :return:
    '''
    observer = Observer()
    # 给watchdog监控，传入变化的处理函数是restart_process
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    # 启动方式：./pymonitor.py app.py
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python3':
        argv.insert(0, 'python3')
    # 更新全局变量command = ['python3', 'app.py']
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)



# 使用效果说明：

'''

给pymonitor.py加上可执行权限，启动服务器，执行：./pymonitor.py app.py
在编辑器中打开一个.py文件，修改后保存，看看命令行输出，是不是自动重启了服务器：
$ ./pymonitor.py app.py
[Monitor] Watching directory /Users/michael/Github/awesome-python3-webapp/www...
[Monitor] Start process python app.py...
...
INFO:root:application (/Users/michael/Github/awesome-python3-webapp/www) will start at 0.0.0.0:9000...
[Monitor] Python source file changed: /Users/michael/Github/awesome-python-webapp/www/handlers.py
[Monitor] Kill process [2747]...
[Monitor] Process ended with code -9.
[Monitor] Start process python app.py...
...
INFO:root:application (/Users/michael/Github/awesome-python3-webapp/www) will start at 0.0.0.0:9000...

'''