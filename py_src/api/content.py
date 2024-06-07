# -*- coding: utf8 -*-
import re
from dataclasses import asdict

from flask import request, jsonify, Blueprint

from py_src.db import project
from py_src.db.project import ProjectDB
from py_src.db.utils import clean
from py_src.test.mock.extern_api_mock import *
from py_src.types import *
# from py_src.api.video_make import init_video_make_data
# from py_src.db import table, video_make_cover, video_make_bg
from py_src.utils.common import get_user_id
from py_src.config import WENXIN_PROMPT_CONTENT
# from py_src.tools.wenxin4 import wenxin_gen


def init_content_api(api_group: Blueprint, service: ServiceMock):
    @api_group.route('/auto_segment', methods=['POST'])
    def auto_segment_api():
        data = request.get_json()
        title = data["title"]
        body = data["body"]
        has_title = data["has_title"]
        sections = service.auto_segment(body, title, has_title)
        res = "\n".join(sections)
        return jsonify(Response(0, "ok", res))

