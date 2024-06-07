def parse_tags(tags):
    if type(tags) == str:
        tags = tags.split(",")
        tags = [x.strip() for x in tags]
        tags = [x for x in tags if x != ""]
    return tags


def get_page_params(req_data):
    page = int(req_data.get("page",0))
    per_page = int(req_data.get("perPage",20))
    return page,per_page
