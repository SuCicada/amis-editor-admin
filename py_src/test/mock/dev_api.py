import os
import random

from flask import Blueprint

from py_src.utils.common import image_path, get_material_type


def init_dev_api(api_group: Blueprint):
    @api_group.get("/images")
    def dev_get_images():
        images = []
        ori = os.listdir(image_path)
        # ori=[x for x in ori if get_material_type(x)=="video"]
        for image in random.sample(ori, 10):
            images.append(image)
        res = []
        for i, image in enumerate(images):
            material_type = get_material_type(image)
            res.append({
                "id": i,
                "image": {
                    "path": image,
                    "type": material_type
                }})
        ress = {
            "data": {
                "count": len(res),
                "rows": res
            }
        }
        return ress
