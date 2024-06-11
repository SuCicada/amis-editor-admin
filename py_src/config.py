import os
import requests
from pathlib import Path

from dotenv import load_dotenv

project_path = Path(__file__).parent.parent
print("Main path", project_path)
image_path = project_path / "db/image"
public_path = project_path / "public"
db_path = project_path / "db"
db_bak_path = db_path / "db_bak"
pages_gen_path = project_path / "pages/gen"
pages_path = project_path / "pages"
site_json_dev_path = project_path / "pages/site.json5"
site_json_prod_path = project_path / "pages/site.prod.json5"
# dub_audio_path = public_path / "dub_audio"
# music_path = public_path / "music"
# if not os.path.exists(dub_audio_path):
#     os.mkdir(dub_audio_path)

DEV = "dev"
PROD = "prod"

# load_dotenv(project_path / ".env")
load_dotenv(project_path / os.getenv("ENV_FILE", ".env.dev"), override=False)
ENVIRONMENT = os.getenv("ENVIRONMENT", PROD)
# IS_DEV = ENVIRONMENT == "dev"
if os.getenv("FLASK_DEBUG", "false") == "false":
    FLASK_DEBUG = False
else:
    FLASK_DEBUG = True
SERVER_PORT = int(os.getenv("SERVER_PORT", 8001))
SITE_JSON_MODE = os.getenv("SITE_JSON_MODE", PROD)
SERVICE_MODE = os.getenv("SERVICE_MODE", PROD)

site_json_path = site_json_dev_path if SITE_JSON_MODE == DEV else site_json_prod_path

IMAGE_SUFFIX = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]
VIDEO_SUFFIX = ["mp4", "mkv", "flv", "avi", "mov", "wmv", "3gp"]

PIC_NUM = 8
WENXIN_PROMPT_SINGLE = "帮我用描述性的话来描述一下以下文案，你只需要生成一个画面就够了，并且字数不要超过40个字。\n\n例如：\n文案：婚姻中，有些男性仿佛受到了某种不可言喻的力量驱使，化身为家中难以应对的'愤怒战士'。\n画面：家庭场景，男性(背影) 在屋子里独自走来走去，看起来烦躁不安。\n\n文案：在心理学领域，这种难以捉摸的力量被称为述情障碍。\n画面：切换至男性与妻子争吵的画面，男性表情愤怒，妻子则显得无奈与困惑。\n\n文案：他们的情感就像埋藏已久的火药，任何一点小摩擦都能引发巨大的爆炸。\n画面：用动画形式表现一个火药桶，每当家中发生一点小摩擦，火药桶就冒火花……\n\n\n现在给定以下文案，请根据上面的形式，生成画面。\n文案：%s\n画面："
WENXIN_PROMPT_CONTENT = """你是抖音自媒体大师，请为{%s}做一个抖音视频脚本，脚本的具体要求是如下：
{脚本要求}=需要把文案内容分成多个镜头，每一个镜头都要有对应的画面（需要描述画面的内容，让人容易寻找对应的图片或视频素材），每一个镜头都要有对应的旁白和文字弹幕，整个视频需要有一个背景音乐(请给出具体的音乐名称)，视频整体要能吸引30-50岁女性观众的眼球，开头5秒必须能抓住30-50岁女性观众，视频大概时⻓1分钟。"""
WENXIN_PROMPT_KEYWORD = """请提取下面文本的关键词，你不需要给出分析过程和思路，直接给我返回关键词结果就可以了！(这是重点重点！) 用","(英文逗号)进行分割。并且，关键词不一定是文本里面的词语，关键词的顺序按照跟文本相关程度进行排序，由高到低。最后，我希望你能够完整的描述画面和场景。
文本：%s
关键词："""

MAX_BATCH_SIZE = 3

