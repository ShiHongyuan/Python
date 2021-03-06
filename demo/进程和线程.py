############### 进程
# 多进程模块：multiprocessing（封装fork），多核并行
# 进程间通讯：每个进程都有全局变量的一个副本，互不影响，但是queue、pipe可以供进程共同读写
# 分布式多进程程序：multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上。
# 原有的进程通信Queue可以继续使用，但是，通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue了

############### 线程
# 多线程模块：Thread，单核并行
# 线程通信：全局变量是所有线程都可以访问的，要线程有自己的局部变量，线程间互不影响，用Threadlocal

# 
