import os
import requests


def proxy_config(http, https=None):
    "代理配置"
    if https is None:
        https = http
    config = {
        "http": http,  # HTTP 代理
        "https": https,  # HTTPS 代理
    }
    return config


def proxy(http, https=None):
    "开启代理"
    if https is None:
        https = http
    data = proxy_config(http, https)
    os.environ["http_proxy"] = data["http"]
    os.environ["https_proxy"] = data["https"]
    print("代理开启!")


def proxy_false():
    "关闭代理"
    os.environ.pop("http_proxy", None)
    os.environ.pop("https_proxy", None)
    print("代理已关闭")


def test_proxy(http, https=None, url="https://dns.google"):
    "测试代理连接"
    if https is None:
        https = http
    data = proxy_config(http, https)
    os.environ["http_proxy"] = data["http"]
    os.environ["https_proxy"] = data["https"]

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("代理连接成功!")
        else:
            print("代理连接失败")
    except requests.exceptions.RequestException as e:
        print(
            f"代理连接失败 {e}",
        )
