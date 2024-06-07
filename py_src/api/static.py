import json

import json5
from flask import send_from_directory, redirect, Flask, request, jsonify
import os

from py_src.config import project_path, DEV, SITE_JSON_MODE, CDN_URL, site_json_prod_path, pages_path, \
    site_json_path
from py_src.types import Response
from py_src.utils.common import get_site_pages


default_new_page = {
    "type": "page",
    "title": "",
    "body": [
    ],
}

web_dist_path = project_path / "amis-editor" / "dist"

def init_static_router(app: Flask):
    @app.route('/')
    def index():
        # print("web_path", web_dist_path)
        return send_from_directory(web_dist_path, 'index.html')

    @app.route('/assets/<path:filename>')
    def web_assets(filename):
        return send_from_directory(web_dist_path / "assets", filename)

    @app.route('/scripts/<path:filename>')
    def web_scripts(filename):
        return send_from_directory(web_dist_path / "scripts", filename)
    @app.route('/img/<path:filename>')
    @app.route('/css/img/<path:filename>')
    def web_img(filename):
        return send_from_directory(web_dist_path / "img", filename)
    # def web_css_img(filename):
    #     print("web_css_img", filename)
    #     return send_from_directory(web_dist_path / "img", filename)
    @app.route('/css/fonts/<path:filename>')
    # def web_css_fonts(filename):
    #     return send_from_directory(web_dist_path / "fonts", filename)
    @app.route('/fonts/<path:filename>')
    def web_fonts(filename):
        return send_from_directory(web_dist_path / "fonts", filename)
    @app.route('/css/<path:filename>')
    def web_css(filename):
        return send_from_directory(web_dist_path / "css", filename)
    @app.route('/<path:filename>.js')
    def web_js2(filename):
        return send_from_directory(web_dist_path , filename+".js")
    @app.route('/js/<path:filename>')
    def web_js(filename):
        return send_from_directory(web_dist_path / "js", filename)

    @app.route("/public/font/<font_name>")
    def public_font(font_name):
        # print(font_name)
        return send_from_directory(project_path / "public/font_repo", font_name)

    @app.route("/public/image_editor/<path:filename>")
    def image_editor_file(filename):
        # print(filename)
        return send_from_directory(project_path / "public/image_editor", filename)

    @app.route("/public/image_editor/image/<path:filename>")
    def image_editor_image_file(filename):
        # print(filename)
        return send_from_directory(project_path / "public/image_editor/image", filename)

    @app.route('/vue-fabric-editor/<path:filename>')
    def vue_fabric_static(filename):
        print(f"Standard request for: {filename}")
        return send_from_directory(project_path / "web/vue-fabric-editor", filename)

    @app.route('/vue-fabric-editor/assets/<path:filename>')
    def vue_fabric_assets_static(filename):
        print(f"Asset request for: {filename}")
        cdn_base_url = CDN_URL + "assets/font/" + filename
        return redirect(cdn_base_url)

    @app.route('/vue-fabric-editor/assets/preview/<path:filename>')
    def vue_fabric_assets_static_svg(filename):
        print(f"Asset preview request for: {filename}")
        cdn_base_url = CDN_URL + "assets/preview/" + filename
        return redirect(cdn_base_url)

    @app.route('/<path:filename>')
    def serve_static(filename):
        print(filename)
        return send_from_directory(project_path, filename)

    @app.route('/image/<path:filename>')
    def serve_static_image(filename):
        # print(filename)
        return send_from_directory(project_path / "db/image", filename)

    @app.route('/pages/site.json')
    def serve_static_site_json():
        # _site_json = ""
        if SITE_JSON_MODE == DEV:
            # _site_json = site_json_dev_path
            pages = get_site_pages()
            for page in pages.values():
                json_path = project_path / page["schemaApi"][1:]
                if not os.path.exists(json_path):
                    with open(json_path, "w", encoding='utf8') as f:
                        new_page = default_new_page
                        new_page["title"] = page["label"]
                        json.dump(new_page, f, indent=2, ensure_ascii=False)
                        print("create new page", json_path)
        # else:
        #     _site_json = site_json_prod_path

        with open(site_json_path, encoding='utf8') as f:
            json5_data = f.read()
            json_data = json5.loads(json5_data)
            return json_data

    @app.get('/pages/schema/<path:name>')
    def get_schema(name: str):
        """
        获取每个菜单项对应的page的schema
        """
        if not name.startswith("/"):
            name = "/" + name
        if name.endswith("/"):
            name = name[:-1]
        print("name", name)
        path = get_site_pages()[name]["schemaApi"]
        path = path[1:] if path.startswith("/") else path
        path = project_path / path

        # path = pages_path / (name + ".json")
        print("get_schema", path)
        with open(path, encoding='utf8') as f:
            json_data = f.read()
            json_data = json5.loads(json_data)
            return jsonify(json_data)

    @app.post('/pages/schema/<path:name>')
    def save_schema(name: str):
        data = request.get_json()
        # data = request_data["data"]
        path = pages_path / (name + ".json")
        print("save_schema", path)
        with open(path, "w", encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            return jsonify(Response(0, "ok", {}))
