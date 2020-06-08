# !/usr/bin/env python3
# -*- coding:utf-8 -*-

' a test pachong '

__author__ = 'shihongyuan'

import requests, json, os, threading, time, logging
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, filename='debug.log')
logging.FileHandler(filename='debug.log', encoding='utf-8')

# 抓取地址
url = 'http://ntce.neea.edu.cn/html1/folder/1507/1260-1.htm'
lxf_url = 'https://www.liaoxuefeng.com/wiki/1016959663602400/1018138223191520'

# 多进程间通讯
# 抓取成功的kv数据
kv_queue = Queue()
# 抓取失败的kv数据
bad_queue = Queue()

# https的请求头
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def htmlParse(content, keys):
    if content and keys:
        for k in keys:
            if k == '日程安排':
                try:
                    # css选择器
                    soup = BeautifulSoup(content, features='html.parser')

                    # 查找class属性等于folderdiv的div，下面的最后一个tr下td下的p的内容
                    data = soup.find_all('meta', attrs={'name': 'description'})
                    kv_queue.put({'日程安排': data[0]['content']})
                    logging.info('content get:  ' + data)
                except Exception:
                    bad_queue.put('日程安排')
                    logging.error('htmlParse error: 日程安排')
                    raise Exception
            else: pass
    else:
        bad_queue.put(keys)
        logging.info('content None')
        return None


'''
请求数据
:param url: 请求地址
:param kv_queue: 抓取成功数据队列
:param bad_queue: 抓取失败数据队列
keys
:return: 
'''
def getData(url, kv_queue, bad_queue, keys):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r and r.status_code == 200:
            # data = htmlParse(r.content.decode(r.encoding))  # encoding有问题，不对
            htmlParse(r.content.decode('utf-8'), keys)
        else:
            logging.error('get ' + url + ' status error')
    except BaseException as e:
        logging.error('getData error')
        raise Exception



def writeDate(kv_queue):
    pass


def running(url, kv_queue, bad_queue, keys):
    logging.info('开始获取...')
    while True:
        logging.info('开始更新...')
        try:
            getData(url, kv_queue, bad_queue, keys)
        except Exception:
            logging.error(str(datetime.datetime.now()) + ' 更新失败...')
        else:
            logging.info('更新结束')
        time.sleep(5)


def retry(url, kv_queue, bad_queue):

    while True:
        k = bad_queue.get(True)
        if k == '日程安排':
            try:
                getData(url, kv_queue, bad_queue, '日程安排')
            except Exception:
                pass
            else:
                break


if __name__ == '__main__':
    keys = ['日程安排']
    server = Process(target=running, args=(url, kv_queue, bad_queue, keys))
    server.daemon = True
    retry_server = Process(target=retry, args=(url, kv_queue, bad_queue))

    server.start()
    server.join()

    time.sleep(3)
    retry_server.start()




