from flask_cors import CORS  # pip install flask_cors
from flask import Flask, request, render_template, redirect, session

# app = Flask(__name__)
app = Flask(__name__, template_folder='./templates', static_folder="./static")
# app = Flask(__name__, template_folder='../static/templates')
app.config['SECRET_KEY'] = 'webPxxsss'

# 解决跨域问题 https://blog.csdn.net/hwhsong/article/details/84959755
CORS(app)


@app.route('/index/')
def index():
    number = session.get('username')
    # 获取当前登录账户用户姓名，学号，密码
    if number:
        for i in admin:
            if i["number"] == number:
                name = i["name"]
                psw = i["psw"]
    else:
        name = None
        psw = None
    print("名字", name, psw)
    return render_template("index.html",
                           name=name,
                           psw=psw,
                           number=number)



if __name__ == '__main__':
    # print(search_stuinfo())
    app.run()
