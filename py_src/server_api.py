import os
import sys
from flask import Blueprint, Flask, make_response

# from .api.gallery_manage import init_api_gallery_manage
from .api.static import init_static_router
from .config import SERVICE_MODE, DEV, ENVIRONMENT

sys.path.append(os.path.dirname(__file__))
# from api.video_make import init_video_make_api, init_video_make_data
from api.content import init_content_api
from api.settings import init_settings_api
from api.table import init_table_api
from .utils.common import *
from .test.mock.extern_api_mock import *

service: ServiceMock

if SERVICE_MODE == DEV:
    service = ServiceMock()
else:
    from .service.extern_api import Service

    service = Service()


def init_api(app: Flask, api_group: Blueprint):
    init_static_router(app)
    init_content_api(api_group, service)
    init_table_api(api_group, service)
    init_settings_api(api_group)
    # init_video_make_api(api_group, service)
    # init_api_gallery_manage(api_group, service.service_images)

    if ENVIRONMENT == DEV:
        from .test.mock.dev_api import init_dev_api
        init_dev_api(api_group)


def trash_api(app: Flask):
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        resp = make_response('Cookie 设置成功！')
        # 设置 cookie，使用 set_cookie 方法
        resp.set_cookie('user_id', 'pengyifu', httponly=True)
        return resp

    @app.route('/api', methods=['POST', 'GET'])
    # @api_group.route('')
    def api():
        data = request.get_json()
        print("/api request", type(data), data)
        # time.sleep(1)
        response_data = {
            'code': 0,
            'msg': 'ok'
        }
        # return jsonify(response_data)
        return response_data

import logging

# 创建日志处理器，输出到标准输出
handler = logging.StreamHandler()
# 设置编码为 utf-8
handler.encoding = 'utf-8'

# 创建日志记录器，并添加处理器
logger = logging.getLogger()
logger.addHandler(handler)

# 设置日志记录器的级别（如果需要）
logger.setLevel(logging.WARNING)

# 使用日志记录器
logger.info("这是一条包含特殊字符的日志消息")

