

def application(environ, stat_response):
    # start_response：一个发送HTTP响应的Header，注意Header只能发送一次
    # start_response()函数接收两个参数，一个是HTTP响应码，一个是一组list表示的HTTP Header，每个Header用一个包含两个str的tuple表示
    stat_response('200 OK', [('Content-Type', 'text/html')])

    # 函数的返回值将作为HTTP响应的Body发送给浏览器
    # 纯英文字母的字节数组不用编码
    return [b'<h1>Hello, web!</h1>']


def application_hasparam(environ, stat_response):
    stat_response('200 OK', [('Content-Type', 'text/html')])

    # environ：一个包含所有HTTP请求信息的dict对象，利用请求参数构造body
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'shihongyuan')  # environ['PATH_INFO'][::]是/Michael，host后面的path信息

    # 函数的返回值将作为HTTP响应的Body发送给浏览器
    # body对象需要编码
    return [body.encode('utf-8')]




