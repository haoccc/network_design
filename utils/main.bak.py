import datetime

from sqlalchemy import create_engine
import configparser
import requests
from sqlalchemy.orm import sessionmaker

import json


def get_author_info(uid, sec_uid):
    """
    访问用户主页，获取关注数、 粉丝数、 获赞数、 作品数、 喜欢数等信息
    :param uid: 用户id
    :param sec_uid: 安全口令
    :return: 返回上述信息字典
    """
    page_url = "https://www.iesdouyin.com/share/user/" + uid + "?did=MS4wLjABAAAA43" \
                                                               "-Yx491gi9LW2aCyRwLvRos9ZUl8Uwd6x73h0vM6kiJzSUfbqVre38T1BqlHxw_&iid" \
                                                               "=MS4wLjABAAAAhvjrUou0FndSpYsrrH7m9MBljp4rU-IJYtns_4pRLuQ&with_sec_did=1&sec_uid" \
                                                               "=" + sec_uid + "&timestamp=1621855955&share_app_name=douyin "

    # json_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=" + sec_uid + "&count=21&max_cursor=0&aid=1128" \
    #                                                                            "&_signature=7a9YGwAAjSdkTmGBA2y3Y" \
    #                                                                            "-2vWA&dytk="
    json_url = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=" + sec_uid
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "referer": page_url
    }
    # print(page_url)
    # print(headers["referer"])

    request = requests.get(json_url, headers)
    json_str = request.text
    json_data = json.loads(json_str)
    # print(json_data)
    author_info = {}
    author_info["total_favorited"] = json_data["user_info"]["total_favorited"]  # 点赞总数
    author_info["aweme_count"] = json_data["user_info"]["aweme_count"]  # 作品数
    author_info["following_count"] = json_data["user_info"]["following_count"]  # 关注数
    author_info["favoriting_count"] = json_data["user_info"]["favoriting_count"]  # 喜欢数
    author_info["follower_count"] = json_data["user_info"]["follower_count"]  # 粉丝数
    author_info["unique_id"] = json_data["user_info"]["unique_id"]  # 抖音号
    author_info["nickname"] = json_data["user_info"]["nickname"]  # 抖音名
    author_info["signature"] = json_data["user_info"]["signature"]  # 首页介绍
    # print(author_info)
    return author_info


def get_video_info(aweme_info):
    """
    获取视频信息
    :param aweme_info: 字典
    :return: 视频信息
    """

    video_info = {}
    video_info["city"] = aweme_info["city"]     # 城市编号
    video_info["desc"] = aweme_info["desc"]     # 视频介绍
    video_info["create_time"] = aweme_info["create_time"]     # 发布时间
    video_info["aweme_id"] = aweme_info["statistics"]["aweme_id"]       # 视频id
    video_info["comment_count"] = aweme_info["statistics"]["comment_count"]     # 评论数
    video_info["digg_count"] = aweme_info["statistics"]["digg_count"]       # 点赞数
    video_info["download_count"] = aweme_info["statistics"]["download_count"]   # 下载数
    video_info["share_count"] = aweme_info["statistics"]["share_count"]     # 分享数
    video_info["share_count"] = aweme_info["statistics"]["share_count"]     # 分享数

    # 视频相关
    video_info["download_addr"] = aweme_info["video"]["bit_rate"][-1]["play_addr"]["url_list"][-1]     # 视频下载地址
    video_info["video_size"] = aweme_info["video"]["bit_rate"][-1]["bit_rate"]      # 视频大小
    video_info["duration"] = aweme_info["video"]["duration"]       # 视频时长

    # 时间戳转换， 使用datetime
    timeStamp = video_info["create_time"]
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    video_info["create_time"] = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    return video_info



def get_info(file_path):
    """
    获取用户信息， 视频信息
    :param file_path: json文件路径
    :return: 0：用户信息， 1：视频信息
    """
    file = open(file_path, "rb")
    data_json = json.load(file)
    data = data_json["data"]  # 视频数据数据信息
    # data_count = len(data)  # 视频信息的个数

    aweme_info_list = []
    comment_list = []
    for single_data in data:
        try:
            aweme_info = single_data["aweme_info"]
            comment_list = single_data["comment_list"]
            # print(aweme_info, comment_list)
            author = aweme_info["author"]
            avater_url = author["avatar_168x168"]["url_list"][-1]  # 头像链接
            sec_uid = author["sec_uid"]  # 用户安全口令
            uid = author["uid"]  # 用户id
            # print(avater_url, uid, sec_uid)
            author_info_dir = get_author_info(uid, sec_uid)  # 获取用户信息
            author_info_dir["gender"] = author["gender"]    #用户性别
            if author["birthday"]:  # 若存在生日信息
                birthday = author["birthday"]
            else:
                birthday = ""
            author_info_dir["birthday"] = birthday
            author_info_dir["birthday"] = birthday

            print(author_info_dir)

            video_info_dir = get_video_info(aweme_info)
            print(video_info_dir)
        except KeyError:
            # 有的只有文字没有视频，没有aweme_info & comment_list字段
            pass
    return author_info_dir, video_info_dir


def write_author_data(author_info_dir, session):



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config.ini', encoding='utf-8')
    username = config.get("database", "username")  # 用户名
    password = config.get("database", "password")  # 密码
    database = config.get("database", "database")  # 数据库
    ip_addr = config.get("database", "ip")  # 数据库

    print(get_info("../data/7_.json"))
    # get_page_info("2550496527406455", "MS4wLjABAAAAqn2_2IVXhUQLwgxmPbUas56kJb-MfOrUyyoJFVHE0AAXLaa2LoOULgqJ8qzf9U9J")

    connect_str = 'mysql+mysqlconnector://' + username + ':' + password + '@' + ip_addr + ':3306/' + database
    print(connect_str)

    # 如果报错 先在命令行执行  easy_install mysql-connector-python
    # 初始化数据库连接:
    engine = create_engine(connect_str)

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()

    # print(engine.table_names())

    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

# html = etree.HTML(request.text)
# # html = etree.parse(request.text, etree.HTMLParser())
# print(html)
# xpa = html.xpath('//span[@class="num"]/text()')
# print(xpa)
# # print(html.xpath("//"))
