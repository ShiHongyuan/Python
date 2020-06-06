# app.py

from flask import Flask, request, render_template

# Flask通过Python的装饰器在内部自动地把URL和函数给关联起来

# 创建Flask的Web框架
app = Flask(__name__)

# 不管是get还是post，url是/的都是访问主页
@app.route('/', methods=['GET', 'POST'])
def home():
    # 框架里不用自己给body编码了
    return render_template('home.html')

# get方法获取登录页面的表单
@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

# post方法返回登录结果
@app.route('/signin', methods=['POST'])
def signin():
    # Flask通过request.form['name']来获取表单的内容
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('signin-ok.html', username = username)
    return render_template('form.html', message="Bad username or password", username=username)


if __name__ == '__main__':
    # 启动Flask的Web框架，Flask自带的Server在端口5000上监听：
    app.run()

    # http://localhost:5000/
    # http://localhost:5000/signin