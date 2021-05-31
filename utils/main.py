# 没有相关包 命令行执行 pip install -r requirements.txt
import datetime
import os

import sqlalchemy
from sqlalchemy import create_engine
import configparser
import requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from utils.table_object import AuthorInfo, VideoInfo
import json

config = configparser.ConfigParser()
config.read('../config.ini', encoding='utf-8')
username = config.get("database", "username")  # 用户名
password = config.get("database", "password")  # 密码
database = config.get("database", "database")  # 数据库
ip_addr = config.get("database", "ip")  # 数据库
avater_path = config.get("path", "avater_path")  # 头像保存路径
video_path = config.get("path", "video_path")  # 视频保存路径


def get_author_info(uid: str, sec_uid: str) -> dir:
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
    # print("page_url", page_url)
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
    author_info["uid"] = uid
    author_info["total_favorited"] = json_data["user_info"]["total_favorited"]  # 点赞总数
    author_info["aweme_count"] = json_data["user_info"]["aweme_count"]  # 作品数
    author_info["following_count"] = json_data["user_info"]["following_count"]  # 关注数
    # author_info["favoriting_count"] = json_data["user_info"]["favoriting_count"]  # 喜欢数
    author_info["follower_count"] = json_data["user_info"]["follower_count"]  # 粉丝数
    author_info["unique_id"] = json_data["user_info"]["unique_id"]  # 抖音号
    author_info["nickname"] = json_data["user_info"]["nickname"]  # 抖音名
    author_info["signature"] = json_data["user_info"]["signature"]  # 首页介绍
    # print(author_info)
    return author_info


def get_video_info(aweme_info: dir) -> dir:
    """
    获取视频信息
    :param aweme_info: 字典
    :return: 视频信息
    """

    video_info = {}
    video_info["city"] = aweme_info["city"]  # 城市编号
    video_info["desc"] = aweme_info["desc"]  # 视频介绍
    video_info["create_time"] = aweme_info["create_time"]  # 发布时间
    video_info["aweme_id"] = aweme_info["statistics"]["aweme_id"]  # 视频id
    video_info["comment_count"] = aweme_info["statistics"]["comment_count"]  # 评论数
    video_info["digg_count"] = aweme_info["statistics"]["digg_count"]  # 点赞数
    video_info["download_count"] = aweme_info["statistics"]["download_count"]  # 下载数
    video_info["share_count"] = aweme_info["statistics"]["share_count"]  # 分享数

    # 视频相关
    video_info["download_addr"] = aweme_info["video"]["bit_rate"][-1]["play_addr"]["url_list"][-1]  # 视频下载地址
    video_info["data_size"] = aweme_info["video"]["bit_rate"][-1]["bit_rate"]  # 视频大小
    video_info["duration"] = aweme_info["video"]["duration"]  # 视频时长

    # 时间戳转换， 使用datetime
    timeStamp = video_info["create_time"]
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    video_info["create_time"] = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    return video_info


class GetAndSave:
    """
    解析json文件，
    数据写入数据库
    下载视频和头像
    """

    def __init__(self, file_path, session: sqlalchemy.orm.session.Session):
        self.file = open(file_path, "rb")
        self.data_json = json.load(self.file)  # 加载数据
        self.data = self.data_json["data"]  # 视频数据数据信息
        self.session = session
        # 多个用户信息列表  多个视频信息列表
        self.author_info_list, self.video_info_list = self.get_info()
        # print("作者", self.author_info_list, "视频", self.video_info_list)
        # print(self.author_info_list[0])

    def get_info(self):
        """
        获取用户信息， 视频信息
        :return: 0：用户信息， 1：视频信息
        """
        author_info_list = []
        video_info_list = []
        for single_data in self.data:
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
                author_info_dir["gender"] = author["gender"]  # 用户性别
                if author["birthday"]:  # 若存在生日信息
                    birthday = author["birthday"]
                else:
                    birthday = None
                author_info_dir["birthday"] = birthday
                author_info_dir["avater_url"] = avater_url
                author_info_list.append(author_info_dir)
                # print(author_info_dir)

                video_info_dir = get_video_info(aweme_info)
                video_info_dir["author_id"] = uid
                video_info_list.append(video_info_dir)
                # print(video_info_dir)
            except KeyError:
                # 有的只有文字没有视频，没有aweme_info & comment_list字段
                pass

        # self.author_info_list = author_info_list
        # self.video_info_list = video_info_list
        return author_info_list, video_info_list

    def write_author_info(self):
        """
        将用户信息写入数据库
        下载用户头像
        :return:
        """
        for single_data in self.author_info_list:
            try:
                info_add = AuthorInfo(author_id=single_data["uid"], name=single_data["nickname"],
                                      unique_id=single_data["unique_id"], cover_path=single_data["uid"] + ".jpeg",
                                      gender=single_data["gender"], birthday=single_data["birthday"],
                                      signature=single_data["signature"],
                                      total_favorited=single_data["total_favorited"],
                                      follower_count=single_data["follower_count"],
                                      following_count=single_data["following_count"],
                                      aweme_count=single_data["aweme_count"])
                self.session.add(info_add)  # 插入数据

                # 下载头像
                url = single_data["avater_url"]
                html = requests.get(url)

                # 图片名 用户id.jpeg
                file_path = os.path.join(avater_path, single_data["uid"] + ".jpeg")
                with open(file_path, "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
                    f.write(html.content)

                try:
                    self.session.commit()
                except IntegrityError as e:
                    session.rollback()
            except IntegrityError:
                pass

    def write_video_info(self):
        """
        将视频信息写入数据库
        下载视频文件
        :return:
        """
        print(self.video_info_list)
        for single_data in self.video_info_list:
            try:
                # 存视频信息到数据库
                info_add = VideoInfo(aweme_id=single_data["aweme_id"], data_size=single_data["data_size"],
                                     create_time=single_data["create_time"], save_path=single_data["aweme_id"] + ".mp4",
                                     digg_count=single_data["digg_count"], comment_count=single_data["comment_count"],
                                     download_count=single_data["download_count"],
                                     description=single_data["desc"],
                                     city=single_data["city"],
                                     author_id=single_data["author_id"],
                                     share_count=single_data["share_count"], duration=single_data["duration"])
                self.session.add(info_add)  # 插入数据

                try:  # 避免主键重复
                    self.session.commit()
                except IntegrityError as e:
                    session.rollback()

                # 下载视频
                url = single_data["download_addr"]
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "close",
                    "Upgrade-Insecure-Requests": "1",
                }

                html = requests.get(url, headers)
                # print(html.text)
                # 视频名 用户id.mp4
                file_path = os.path.join(video_path, single_data["aweme_id"] + ".mp4")
                # print(file_path)
                with open(file_path, "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
                    f.write(html.content)  # html.content 获取内容
            except IntegrityError:
                pass


if __name__ == '__main__':
    # print(get_info("7_.json"))
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
    print(type(session))
    print(engine.table_names())

    x = GetAndSave("../data/7_.json", session=session)
    # x.get_info()
    print("----------------------------------------------------------")
    x.write_video_info()
    x.write_author_info()

    # # 提交即保存到数据库:
    # session.commit()
    # # 关闭session:
    # session.close()
