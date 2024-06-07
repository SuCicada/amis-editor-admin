# -*- coding: utf8 -*-

import os
import sys

from flask import Flask, Blueprint
from flask_cors import CORS

sys.path.append(os.path.join(os.path.dirname(__file__), "py_src"))
from py_src.config import Path, FLASK_DEBUG
from py_src.utils.common import init
from py_src.config import db_path, SERVER_PORT

def main():

    # def get_args():
    #     parser = argparse.ArgumentParser(description="My Command Line Tool")
    #     parser.add_argument( '--env', type=str, help="environment: dev/prod")
    #     # parser.add_argument('-o', '--output', type=str, help="Output file")
    #     # parser.add_argument('--verbose', action='store_true', help="Enable verbose mode")
    #
    #     # 解析命令行参数
    #     args = parser.parse_args()
    #     return args
    #
    # args = get_args()

    # def set_env():
    #     if args.env == "dev":
    #         common.ENVIRONMENT = "dev"
    # print("IS_DEV", IS_DEV)

    if not os.path.exists(os.path.join(db_path)):
        os.mkdir(os.path.join(db_path))

    from py_src.server_api import init_api

    project_root = Path(__file__).parent
    app = Flask(__name__)
    app.static_folder = project_root

    CORS(app, expose_headers=["Content-Disposition"], resources={
        "*": {
            "origins": [
                '*',
                # 'http://localhost:58760',
                # 'http://localhost:58761',
                # 'http://localhost:3001',
                # 'http://localhost:3000',
                # 'http://localhost:10930',
                # 'http://localhost:1024',
            ],
            "methods": ["GET", "HEAD", "PUT", "PATCH", "POST", "DELETE"],
            "supports_credentials": False,
        }
    })

    init()
    api_group = Blueprint('api', __name__, url_prefix='/api')
    init_api(app, api_group)
    app.register_blueprint(api_group)


    debug = FLASK_DEBUG
    # debug = True
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=debug)

if __name__ == '__main__':
    # app.get
    main()
