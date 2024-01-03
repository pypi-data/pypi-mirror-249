import time
import requests


def get(api_url, headers=None):
    "get请求"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("报错:", e)
        print("响应内容:", response.text)
        return None


def post(api_url, json=None, headers=None):
    "post请求"
    try:
        response = requests.post(api_url, json=json, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("报错:", e)
        print("响应内容:", response.text)
        return None


def get_retry(url, max_retries=10, sleep=60):
    "get请求, 自动重试"
    retries = 0
    while retries < max_retries:
        api_data_dl = get(url)  # 获取数据

        if api_data_dl:  # 如果成功获取到数据
            return api_data_dl

        retries += 1
        print(f"重试 {retries}/{max_retries} - 请求失败.正在重试...")
        time.sleep(sleep)  # 等待

    print("达到最大重试次数.无法获取数据.")
    return None


def get_remote_file_size(url, max_retries=5):
    "获取远程文件大小"
    retries = 0
    while retries < max_retries:
        try:
            response = requests.head(url)
            if response.status_code == 200 and "Content-Length" in response.headers:
                return int(response.headers["Content-Length"])
            else:
                return None
        except Exception as e:
            retries += 1
            print(f"尝试重新连接 ({retries}/{max_retries})...{e}")

    print(f"无法获取远程文件大小，已达到最大重试次数 ({max_retries}次)")
    return None


def message_status(data, message=None, code=None):
    "消息模板"
    if not data:
        if code is None:
            code = 400
        if message is None:
            message = "请求错误"
    else:
        code = 200
        message = "请求成功"
    return {"code": code, "message": message, "data": data}


def check_remote_file_existence(url):
    "检查远程文件是否存在"
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False
