import configparser
import json
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests

# https://apis.map.qq.com/ws/district/v1/list?key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77
# 所有行政区信息 包括省份


config = configparser.ConfigParser()
config.read('../config.ini', encoding='utf-8')
username = config.get("database", "username")  # 用户名
password = config.get("database", "password")  # 密码
database = config.get("database", "database")  # 数据库
ip_addr = config.get("database", "ip")  # 数据库


def get_city(city_code: int):
    """
    获取城市编号对应的 市级 名字
    :param city_code: 城市编号
    :return: 市名
    """
    try:
        code_url = "https://restapi.amap.com/v3/config/district?keywords=" + str(
            city_code) + "&subdistrict=2&key=d3e0738f6c1b797a2161818a50ab6543"  # 调用获取城市编码
        code_request = requests.get(code_url)
        code_html = code_request.text  # 得到返回的json格式数据
        # print(code_html)
        code_target = json.loads(code_html)  # 解析json
        city_name = code_target['districts'][0]['name']  # 获取所在城市的编码
    except:
        city_name = None
    # print(city_name)
    return city_name


class DataVisualization:
    """
    数据可视化
    """

    def __init__(self, session: sqlalchemy.orm.session.Session = None):
        """
        可选传入数据库连接
        :param session:
        """
        if session is None:     # 如果未建立连接，则连接
            connect_str = 'mysql+mysqlconnector://' + username + ':' + password + '@' + ip_addr + ':3306/' + database
            # 初始化数据库连接:
            engine = create_engine(connect_str)
            # 创建DBSession类型:
            DBSession = sessionmaker(bind=engine)
            # 创建session对象:
            self.session = DBSession()
        else:
            self.session = session

        self.user_count = 0
        self.video_count = 0

    def get_user_count(self):
        """
        获取数据库中现有用户数
        :return: user_count
        """
        query = "select count(*) from author_info"
        cursor = self.session.execute(query)
        result = cursor.fetchall()[0][0]
        self.user_count = result
        return result

    def get_video_count(self):
        """
        获取数据库中现有视频数
        :return: user_count
        """
        query = "select count(*) from video_info"
        cursor = self.session.execute(query)
        result = cursor.fetchall()[0][0]
        self.video_count = result
        return result

    def get_age_distribution(self):
        """
        00、90、80、70及以前个年龄段人数
        :return: [count_00, count_90, count_80, count_70]
        """
        # 00后人数
        query = "select count(*) from author_info where birthday >= '2000-01-01'"
        cursor = self.session.execute(query)
        count_00 = cursor.fetchall()[0][0]

        # 90后人数
        query = "select count(*) from author_info where birthday >= '1990-01-01' and birthday < '2000-01-01'"
        cursor = self.session.execute(query)
        count_90 = cursor.fetchall()[0][0]

        # 80后人数
        query = "select count(*) from author_info where birthday >= '1980-01-01' and birthday < '1990-01-01'"
        cursor = self.session.execute(query)
        count_80 = cursor.fetchall()[0][0]

        # 70后及以前
        query = "select count(*) from author_info where birthday < '1980-01-01'"
        cursor = self.session.execute(query)
        count_70 = cursor.fetchall()[0][0]
        return [count_00, count_90, count_80, count_70]

    def get_city_distribution(self):
        """
        获取 用户数最多的前10个城市，其余归为其他
        :return: {"city1":count, "city2":count, "city3":count,, "city4":count, "city5":count,
        "city6":count, "city7":count, "othercity":count}
        """
        if self.video_count == 0:  # 先确定视频总数
            self.get_video_count()
        query = "select city, count(*) from video_info group by city desc limit 10"  # 城市编号 对应数目
        cursor = self.session.execute(query)
        result = cursor.fetchall()  # [(city_code, count), (city_code, count), (city_code, count)````]

        other_count = self.get_video_count() - sum([i[1] for i in result])  # 其他城市的数量 内置函数+列表推导式
        # print("other", other_count)

        # {城市名：数量}
        result_dir = {"other_city": other_count}
        for single in result:
            # single = (city_code, count)
            city_name = get_city(single[0])
            result_dir[city_name] = single[1]
        # print(result)

        result_dir = sorted(result_dir.items(), key=lambda item: item[1], reverse=True)  # 对输出结果按照大到小排序
        # print("结果", result_dir)
        return result_dir

    def get_post_time_distribution(self):
        """
        视频发布时间统计
        :return:
        """
        hour_count_list = [0 for i in range(24)]    # 分别代表24个时间段， 预制为0
        query = "select create_time from video_info"
        cursor = self.session.execute(query)
        query_result = cursor.fetchall()
        for single in query_result:     # 遍历查询结果
            hour = int(single[0].strftime("%H"))    # 获取发布时间里的小时
            hour_count_list[hour-1] += 1    # 对应小时加一
        # print(hour_count_list)
        return hour_count_list

    def session_close(self):
        """
        关闭数据库连接
        :return:
        """
        self.session.close()


if __name__ == '__main__':
    print(get_city(440100))
    xx = DataVisualization()
    xx.get_user_count()
    print(xx.get_age_distribution())
    xx.get_city_distribution()
    xx.get_post_time_distribution()
    xx.session_close()