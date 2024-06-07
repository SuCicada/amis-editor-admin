import base64
import time
from pprint import pprint
from typing import Dict, List, Tuple

from py_src.types import Segmentation, VideoMakeForm, Response
from deprecated import deprecated


class ServiceMock:

    def write_your_api_here(self, data: Dict) -> Response:
        """
        Write your api here
        :param data:
        :return:
        """
        return Response(0, "ok", data)

