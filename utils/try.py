import os

import requests


def get_avater():
    url = "https://p3.douyinpic.com/img/tos-cn-avt-0015/650cb50ff45820be9e79d2fe6135cf51~c5_168x168.jpeg?from=116350172"

    html = requests.get(url)
    with open("../avater/1.jpeg", "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
        f.write(html.content)


# def read_file():
#     f = open("../data/fiddler自动保存.json", "r", encoding="utf-8")
#     line = f.readline()
#     while line:
#         print(line, end=" ")  # 在 Python 3 中使用
#         line = f.readline()


def get_json_data(file_path, save_dire):
    """
    提取json数据
    :param file_path: 原始报文文件
    :param save_dire: json文件保存文件夹
    :return:
    """
    f = open(file_path, "rb")
    line = f.readline()
    save_name = "json_data.json"    # 保存json文件的后缀名
    count = 1   # 计数&文件名区分
    while line:
        ss = line.decode("utf-8")
        if "Response body: {" in ss:    # 如果是有数据的响应体
            name = str(count) + save_name   # 保存json的文件名
            count += 1
            write_file = open(os.path.join(save_dire, name), "w", encoding="utf-8")
            result = ss.split("Response body: ")[-1]    # 获取 Response body: 后的字符串
            # print(result)
            write_file.write(result)
            write_file.close()
        line = f.readline()


if __name__ == '__main__':
    # get_avater()
    get_json_data("../data/fiddler自动保存.json", "../data/")
