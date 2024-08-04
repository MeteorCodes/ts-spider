import requests
import csv
import json
import random


def download_file(url, output_filename, csv_file_path):
    """
    从 CSV 文件加载代理池，转换为 JSON 格式，并使用代理池下载文件。

    :param url: 文件的下载地址
    :param output_filename: 保存文件的路径
    :param csv_file_path: CSV 文件路径
    """
    proxies_list = []

    # 读取 CSV 文件并将其转换为代理池列表
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                proxy = {
                    "http": f"http://{row['代理IP地址']}:{row['端口']}"
                }
                proxies_list.append(proxy)
    except UnicodeDecodeError:
        # 如果 utf-8 编码失败，尝试使用 gbk 编码
        with open(csv_file_path, mode='r', encoding='gbk') as file:
            reader = csv.DictReader(file)
            for row in reader:
                proxy = {
                    "http": f"http://{row['代理IP地址']}:{row['端口']}"
                }
                proxies_list.append(proxy)

    # 将代理列表转换为 JSON 格式并保存到临时 JSON 文件
    json_file_path = 'temp_proxies.json'
    with open(json_file_path, mode='w', encoding='utf-8') as file:
        json.dump({"proxies": proxies_list}, file, indent=4, ensure_ascii=False)

    max_retries = len(proxies_list)  # 最大重试次数等于代理池的长度

    for attempt in range(max_retries):
        proxy = random.choice(proxies_list)  # 随机选择一个代理
        print(f"尝试使用代理: {proxy}")

        try:
            # 发送GET请求
            response = requests.get(url, proxies=proxy, timeout=10)  # 设置超时时间
            response.raise_for_status()  # 检查请求是否成功

            # 将内容写入文件
            with open(output_filename, 'wb') as file:
                file.write(response.content)

            print(f"文件已成功下载到: {output_filename}")
            return  # 成功下载后退出函数

        except requests.RequestException as e:
            print(f"下载失败 ({attempt + 1}/{max_retries}): {e}")
            # 如果所有代理都失败了，可以在这里添加更多的处理逻辑，如记录失败信息

    print("所有代理尝试失败，下载未成功。")
