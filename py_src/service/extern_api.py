import os
import re
from pprint import pprint
from typing import Dict

from py_src.test.mock.extern_api_mock import ServiceMock
from py_src.types import Response


class Service(ServiceMock):
    def write_your_api_here(self, data: Dict) -> Response:
        """
        Write your api here
        :param data:
        :return:
        """
        return Response(0, "ok", data)
