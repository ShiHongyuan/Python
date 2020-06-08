# https现在大部分网站都增加了安全验证
# 请求时，提供一个headers
import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url = 'https://www.douban.com/'
r = requests.get(url, headers=headers)

