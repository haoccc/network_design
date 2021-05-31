import requests


def get_avater():
    url = "https://p3.douyinpic.com/img/tos-cn-avt-0015/650cb50ff45820be9e79d2fe6135cf51~c5_168x168.jpeg?from=116350172"

    html = requests.get(url)
    with open("../avater/1.jpeg", "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
        f.write(html.content)


if __name__ == '__main__':
    get_avater()