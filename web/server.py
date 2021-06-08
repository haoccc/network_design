import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.main import get_json_interface   # 获取给定关键词视频
from utils.main import GetAndSave   # 获取给定关键词视频
from flask_cors import CORS  # pip install flask_cors
from flask import Flask, request, render_template, redirect, session

# app = Flask(__name__)
app = Flask(__name__, template_folder='./templates', static_folder="./static")
# app = Flask(__name__, template_folder='../static/templates')
app.config['SECRET_KEY'] = 'webPxxsss'

# 解决跨域问题 https://blog.csdn.net/hwhsong/article/details/84959755
CORS(app)

config = configparser.ConfigParser()
config.read('../config.ini', encoding='utf-8')
username = config.get("database", "username")  # 用户名
password = config.get("database", "password")  # 密码
database = config.get("database", "database")  # 数据库
ip_addr = config.get("database", "ip")  # 数据库
avater_path = config.get("path", "avater_path")  # 头像保存路径
show_path = config.get("path", "video_path")  # 视频保存路径
search_video_path = config.get("path", "search_video_path")  # 视频保存路径


connect_str = 'mysql+mysqlconnector://' + username + ':' + password + '@' + ip_addr + ':3306/' + database
print(connect_str)
engine = create_engine(connect_str)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


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


@app.route('/')
def root():
    return render_template("try_video.html")


# 所有视频展示接口
@app.route('/video_show/', methods=['GET', 'POST'])
def video_show():
    """
    所有视频展示接口
    :return:
    """
    show_video_list = os.listdir(show_path)
    video_path = [os.path.join("../../../video/", i) for i in show_video_list]
    print(request.json)
    print(request.values)
    if request.method == "POST":
        offset = int(request.form.get("offset"))
        count = int(request.form.get("count"))
        # print(request.values)
        print(offset, count)
        if offset + count > len(video_path):
            result = video_path[offset:]
            cyc_count = int(len(result) / 5)
            remain = len(result) % 5
        elif offset >= len(video_path):
            return "到底了"
        else:
            result = video_path[offset: offset + count]
            cyc_count = int(len(result) / 5)
            remain = len(result) % 5
        # 除去列表中的 []'
        result.append(str(cyc_count))
        result.append(str(remain))
        result = str(result)
        result = result.replace("'", "")
        result = result.replace("[", "")
        result = result.replace("]", "")
        print(result)
        return result
    else:
        return "请求方式错误"


# 关键词 搜索视频接口
@app.route('/search_video/', methods=['GET', 'POST'])
def search_video():
    """
    关键词 搜索视频接口
    :return:
    """
    offset = 10    # 默认从10开始 从0开始无法指定 count值
    count = 5
    if request.method == "POST":
        keyword = request.form.get("keyword")
        # count = request.form.get("count")
        print(keyword)
        xx = GetAndSave(get_json_interface(keyword=keyword, offset=offset, count=count),
                        session=session, video_path=search_video_path)
        result = xx.write_video_info()   # 下载 写入视频

        # 除去列表中的 []'
        result = str(result)
        result = result.replace("'", "")
        result = result.replace("[", "")
        result = result.replace("]", "")
        print("搜索关键词的结果：", result)
        return result
    return None




if __name__ == '__main__':
    # print(search_stuinfo())
    app.run()
