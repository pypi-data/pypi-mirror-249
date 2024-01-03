from datetime import datetime, timedelta
import jwt


def token(secret_key, payload, exp=None):
    "生成token"
    payload = {
        "exp": exp or datetime.utcnow() + timedelta(days=30),  # 设置过期时间
    }
    data = jwt.encode(payload, secret_key, algorithm="HS256")
    return data


def verify_token(token, secret_key):
    "验证token是否过期失效"
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        # 检查令牌是否过期
        if (
            "exp" in payload
            and datetime.utcfromtimestamp(payload["exp"]) > datetime.utcnow()
        ):
            return True
    except jwt.ExpiredSignatureError:
        # 令牌过期
        return False
    except jwt.DecodeError:
        # 令牌验证失败
        return False


def decode_token(token, secret_key):
    "解密token"
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 令牌已过期
    except jwt.InvalidTokenError:
        return None  # 无效令牌
