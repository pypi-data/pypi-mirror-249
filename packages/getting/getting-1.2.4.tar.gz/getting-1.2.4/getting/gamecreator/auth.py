from ..response import get, post


def login_pw(username, password):
    "使用账号密码登录GC平台并获取信息"
    # 获取token
    url = "https://www.gamecreator.com.cn/index.php/apis/user/passwordlogin"
    json = {"username": username, "password": password}
    data = post(url, json)
    if data.get("code") == 20000:
        # 获取信息
        data = data.get("data")
        token = data.get("token")
        data = login_token(token)
    else:
        data = None
    return data


def login_token(token):
    "使用token登录GC平台并获取信息"
    url = "https://www.gamecreator.com.cn/index.php/apis/user/getuserinfo"
    headers = {"Token": token}
    data = get(url, headers)
    if data.get("code") != 20000:
        data = None
    return data


def get_level(uid):
    "根据uid获取账号等级"
    url = "https://www.gamecreator.com.cn/index.php/apis/redismag/get_user_actives"
    json = {"uid": uid}
    data = post(url, json)
    if data.get("code") != 20000:
        data = None
    return data
