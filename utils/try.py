import os
import urllib.parse
import requests


def get_avater():
    url = "https://p3.douyinpic.com/img/tos-cn-avt-0015/650cb50ff45820be9e79d2fe6135cf51~c5_168x168.jpeg?from=116350172"

    html = requests.get(url)
    with open("../avater/1.jpeg", "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
        f.write(html.content)


def get_json_data(file_path, save_dire):
    """
    提取json数据
    :param file_path: 原始报文文件
    :param save_dire: json文件保存文件夹
    :return:
    """
    f = open(file_path, "rb")
    line = f.readline()
    save_name = "json_data.json"  # 保存json文件的后缀名
    count = 1  # 计数&文件名区分
    while line:
        ss = line.decode("utf-8")
        if "Response body: {" in ss:  # 如果是有数据的响应体
            name = str(count) + save_name  # 保存json的文件名
            count += 1
            write_file = open(os.path.join(save_dire, name), "w", encoding="utf-8")
            result = ss.split("Response body: ")[-1]  # 获取 Response body: 后的字符串
            # print(result)
            write_file.write(result)
            write_file.close()
        line = f.readline()


def try_interface():
    """

    :return:
    """
    url = "https://aweme.snssdk.com/aweme/v1/general/search/single/?ts=1622647849&js_sdk_version=1.16.3.5&app_type" \
          "=normal&os_api=25&device_platform=android&device_type=TAS-AN00&iid=2375404505035863&ssmix=a" \
          "&manifest_version_code=630&dpi=320&uuid=863064127152041&version_code=630&app_name=aweme&version_name=6.3.0" \
          "&openudid=90875a3ea1bfd6c4&device_id=70788060545102&resolution=900*1600&os_version=7.1.2&language=zh" \
          "&device_brand=HUAWEI&ac=wifi&update_version_code=6302&aid=1128&channel=wandoujia_aweme1&_rticket" \
          "=1622647850383&mcc_mnc=46007 "
    headers = {
        "X - SS - STUB": "FC2BE98CDD739473F9F38CBD6A806EDC",
        "Accept - Encoding": "gzip",
        "X - SS - REQ - TICKET": "1622647850381",
        "sdk - version": "1",
        "Cookie": "odin_tt"
                  "=cfde8ffa06fd8b62728be1f8edef8423c91a378ee03c2a753293c89467ceba43c36d50ffcae9e5eac2242b574748ac19813261923c43932542e3d1491a7a58f6; install_id=2375404505035863; ttreq=1$728f7db15f30087aba9fd56b8ef022530a19de40; qh[360]=1",
        "X-Gorgon": "03006cc0440092403beeaad37b8f0af481db470890fcbfa98b4c",
        "X-Khronos": "1622647850",
        # "X-Pods": " ",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content - Length": "182",
        "Host": "aweme.snssdk.com",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/3.10.0.1"
    }
    data = "keyword=%E5%AD%A6%E4%B9%A0&offset=40&count=30&is_pull_refresh=0&search_source=normal_search&hot_search=0&latitude=37.00125&longitude=112.56358166666665&search_id=&query_correct_type=1"

    html = requests.post(url, data=data, headers=headers)
    # print(html.text)
    f = open("a.txt", "wb")
    f.write(html.content)


def get_json_interface(keyword: str, offset: int, count: int = 50, save_path: str = None):
    """
    调用接口获取指定内容的 相关视频 信息
    :param keyword: 检索关键词
    :param offset: 偏移值
    :param count: 每页数量 默认50
    :param save_path: 数据保存路径 默认None
    :return:
    """
    url = "https://aweme.snssdk.com/aweme/v1/general/search/single/?ts=1622647849&js_sdk_version=1.16.3.5&app_type" \
          "=normal&os_api=25&device_platform=android&device_type=TAS-AN00&iid=2375404505035863&ssmix=a" \
          "&manifest_version_code=630&dpi=320&uuid=863064127152041&version_code=630&app_name=aweme&version_name=6.3.0" \
          "&openudid=90875a3ea1bfd6c4&device_id=70788060545102&resolution=900*1600&os_version=7.1.2&language=zh" \
          "&device_brand=HUAWEI&ac=wifi&update_version_code=6302&aid=1128&channel=wandoujia_aweme1&_rticket" \
          "=1622647850383&mcc_mnc=46007 "

    headers = {
        "X - SS - STUB": "FC2BE98CDD739473F9F38CBD6A806EDC",
        "Accept - Encoding": "gzip",
        "X - SS - REQ - TICKET": "1622647850381",
        "sdk - version": "1",
        "Cookie": "odin_tt"
                  "=cfde8ffa06fd8b62728be1f8edef8423c91a378ee03c2a753293c89467ceba43c36d50ffcae9e5eac2242b574748ac19813261923c43932542e3d1491a7a58f6; install_id=2375404505035863; ttreq=1$728f7db15f30087aba9fd56b8ef022530a19de40; qh[360]=1",
        "X-Gorgon": "03006cc0440092403beeaad37b8f0af481db470890fcbfa98b4c",
        "X-Khronos": "1622647850",
        # "X-Pods": " ",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content - Length": "182",
        "Host": "aweme.snssdk.com",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/3.10.0.1"
    }
    keyword = urllib.parse.quote(keyword)
    data = "keyword=%s&offset=%d&count=%d&is_pull_refresh=0&search_source=normal_search&hot_search=0&latitude=37" \
           ".00125&longitude=112.56358166666665&search_id=&query_correct_type=1 " % (keyword, offset, count)
    print(data)
    html = requests.post(url, data=data, headers=headers)
    # print(html.text)
    if save_path:   # 给了路径，就保存为文件
        f = open(save_path, "wb")
        f.write(html.content)
    else:   # 直接返回数据
        return html.text


if __name__ == '__main__':
    # get_avater()
    # get_json_data("../data/fiddler自动保存.json", "../data/")
    get_json_interface("学习", 10, 10)
