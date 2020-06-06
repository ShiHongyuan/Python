# app.py

from flask import Flask, request

# Flask通过Python的装饰器在内部自动地把URL和函数给关联起来

# 创建Flask的Web框架
app = Flask(__name__)

# 不管是get还是post，url是/的都是访问主页
@app.route('/', methods=['GET', 'POST'])
def home():
    # 框架里不用自己给body编码了
    return '<h1>Home</h1>'

# get方法获取登录页面的表单
@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
                <p><label>name:</label><input name="username"></p>
                <p><label>password:<label><input name="password"></p>
                <p><button type="submit">Sign In</button></p>
            </form>'''

# post方法返回登录结果
@app.route('/signin', methods=['POST'])
def signin():
    # Flask通过request.form['name']来获取表单的内容
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'


if __name__ == '__main__':
    # 启动Flask的Web框架，Flask自带的Server在端口5000上监听：
    app.run()

    # http://localhost:5000/
    # http://localhost:5000/signin







