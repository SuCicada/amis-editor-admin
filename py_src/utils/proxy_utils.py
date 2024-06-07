import os
from functools import wraps

proxy_protocol = "socks5"                       # 设置代理
proxy_host = "127.0.0.1"
proxy_port = 20808


def proxy_decorator(func):
    '''通过代理访问国外网站'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 设置代理
        os.environ["ALL_PROXY"] = f"{proxy_protocol}://{proxy_host}:{proxy_port}"
        # 调用被装饰的函数
        result = func(*args, **kwargs)
        # 取消代理设置
        os.environ["ALL_PROXY"] = ""
        return result
    return wrapper