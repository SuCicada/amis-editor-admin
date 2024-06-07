# -*- coding: utf8 -*-
import json
import os
import time
import io
import requests

from py_src.tools.baidu_translate import translate
from pydub import AudioSegment
from py_src.tools.generate import run
import tempfile

import random
import datetime
import string
from zhon import hanzi
import numpy as np

from py_src.utils.common import IMAGE_SUFFIX, VIDEO_SUFFIX
from py_src.tools.long_form_text_synthesis import LongTextSynthesizer
from py_src.tools.final_crawl import get_max_prob_keyword, keywords_vector

from py_src.tools.peiyin_download import generate

from pathlib import Path
from py_src.db.project import update_current_project_progress
from py_src.tools.tencent_cdn import upload_output_video


import re
import gc
import moviepy.editor as mp
from PIL import Image
from py_src.tools.video_effects import DESIRED_HEIGHT, transition, FPS

FONT_DIR = r"public/script_font"

punctuation = hanzi.punctuation + string.punctuation + " "


def split_text_by_symbols(text, punctuation):
    """按照标点符号进行文本分割(包含标点)"""
    res = [""]
    for char in text:
        if char in punctuation:
            if char not in string.whitespace:
                res[-1] += char
            res.append("")
        else:
            res[-1] += char
    return res

def merge_strings(strings, length, save_punc=True, title='', read_title=False):
    """合并字符串"""
    result = []
    res = []
    current_string = ""
    idx = 0  # 第一个一般是标题
    while idx < len(strings):
        cur_string = strings[idx].strip().strip("\n")
        if length <= len(current_string + cur_string) <= 2 * length:
            result.append(current_string + cur_string)
            current_string = ""
        elif len(current_string + cur_string) < length:
            current_string += cur_string
        elif current_string and len(current_string + cur_string) > 2 * length:
            result.append(current_string)
            current_string = cur_string
        else:
            result.append(cur_string)
        idx += 1

    if current_string:  # 如果最后的current_string有剩余，则将其添加到result列表中
        result.append(current_string)

    if len(result[0]) < length:  # 专门处理result的第一个元素
        res.append(result[0])
    else:
        res.append(result[0])

    for idx in range(1, len(result)):
        if len(result[idx]) < length and res:
            res[-1] += result[idx]
        else:
            res.append(result[idx])

    if not save_punc:
        last_res = []
        for idx in range(len(res)):
            ttt = res[idx]
            if not res[idx]: continue
            if res[idx][0] in punctuation:
                res[idx] = res[idx][1:]
            if not res[idx]: continue
            if res[idx][-1] in punctuation:
                ttt = res[idx][: -1]
            last_res.append(ttt)
        res = last_res
    if read_title:
        res.insert(0, title)
    for t in range(len(res)):
        if res[t][0] == "。":
            res[t] = res[t][1:]
    return res

def regex_text(article, punctuation, read_title, title):
    return merge_strings(split_text_by_symbols(article.replace("\n", "。"), punctuation.replace("、", "").replace("《", "").replace("》", "").replace("‘", "").replace("’", "").replace("'", "").replace('"', "").replace("【", "").replace("】", "").replace("(", "").replace(")", "").replace("（", "").replace("）", "").replace("[", "").replace("]", "").replace("=", "").replace("“", "").replace("”", "").replace("+", "").replace("-", "").replace("-", "").replace(".", "").replace("%", "").replace("*", "").replace("/", "").replace("×", "")), 15, title=title, read_title=read_title)


def get_script(split_text, length=17):
    split_text = "".join(split_text)
    if split_text[0] in punctuation:
        split_text = split_text[1:]
    if split_text[-1] in punctuation:
        split_text = split_text[: -1]

    if len(split_text) > length:
        script_text = split_text[: length] + "\n" + split_text[length:]
    elif len(split_text) > 2 * length:
        script_text = split_text[: length] + "\n" + split_text[length: 2 * length] + "\n" + split_text[2 * length:]
    else:
        script_text = split_text
    return script_text

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def detect_language(text):
    # 计算文本中中文字符的比例
    chinese_count = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    english_count = sum(1 for char in text if 'a' <= char.lower() <= 'z')

    # 判断是中文还是英文
    if chinese_count > english_count:
        return "Chinese"
    elif english_count > chinese_count:
        return "English"
    else:
        return "Other"

def get_keyword_from_url(text):
    """解析cos里英文关键词"""
    text = text.strip("/")
    text = text.split("/")[-1]
    return text


def get_material(has_keyword, material_path, used_images, keyword_list, use_ai)->(str, str):
    """
    :return: material name, material type
    """
    res_type: str = ""

    while True:
        try:
            if not has_keyword:
                times = 3
                while times >= 0:
                    if material_path.endswith("json"):
                        with open(material_path, "r", encoding="utf8") as json_file:
                            data = dict(json.load(json_file)).popitem()[1]
                            image = random.choice(data)
                    else:
                        image = random.choice([os.path.join(material_path, img) for img in os.listdir(material_path)])

                    if image not in used_images:
                        used_images.append(image)
                        break
                    else:           # 有可能数据库里面图片不太够
                        if times <= 0:
                            used_images.append(image)
                        times -= 1
            else:
                # keyword_dict = dict()
                # keywords = list(set([p.strip("_video") for p in os.listdir(material_path)]))
                for keyword in random.choices(keyword_list, k=8):
                    try:
                        if material_path.endswith("json"):
                            with open(material_path, "r", encoding="utf8") as json_file:
                                data = dict(json.load(json_file))
                                key = f"{data.popitem()[0].split('/')[0]}/{keyword}/"
                                if key not in data:
                                    continue
                                image = random.choice(data[key])
                        else:
                            image = os.path.join(material_path, keyword,
                                             random.choice(os.listdir(os.path.join(material_path, keyword))))
                        print(f"关键词为：{keyword}".ljust(20), end="\t")
                        if image in used_images:
                            raise Exception()
                        break
                    except:
                        print(f"{keyword}当前关键词不在！或者这张图片已经用过了！")
            ends = image.split(".")[-1]
            if ends in IMAGE_SUFFIX:
                # print("！", end="\t")
                res_type = "image"
                if use_ai:
                    image = run(image, ["(((asian)))"], controlnet=False)

            elif ends in VIDEO_SUFFIX:
                # print("\t处理视频！", end="\t")
                res_type = "video"
                # raise Exception()
            else:
                continue
            print("\t素材处理成功！", end="\t")
            break
        except Exception as e:
            print("素材处理出现了错误！", e)
            time.sleep(1)
    return image, res_type


def generate_ms_audio(voice_name, script_texts, express="peace"):
    """生成配音"""
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d ")
    audio_path = os.path.join("db", "dub", "_".join([today_str, voice_name, sanitize_filename(script_texts[0].strip("\n").strip())]))
    if not os.path.exists(audio_path) or not os.listdir(audio_path):
        voice, rate = (voice_name, "1.05")
        s = LongTextSynthesizer(subscription="05b318f376b6417d835a3dfcf7a72332", region="eastus", voice=voice)

        for idx, text in enumerate(script_texts):
            s.synthesize_text(idx, text=text, rate=rate, express=express, output_path=Path(audio_path))
    audios_paths = [os.path.join(audio_path, a) for a in os.listdir(audio_path)]
    return audio_path, audios_paths

def generate_my_audio(voice_name, script_texts, express="peace"):
    """生成网红配音"""
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d ")
    audio_path = os.path.join("db", "dub",
                              "_".join([today_str, voice_name, sanitize_filename(script_texts[0].strip("\n").strip())]))
    if not os.path.exists(audio_path) or not os.listdir(audio_path):
        voice, rate = (voice_name, "1.00")
        for idx, text in enumerate(script_texts):
            generate(idx, text, voice, express, audio_path)
    audios_paths = [os.path.join(audio_path, a) for a in os.listdir(audio_path)]
    return audio_path, audios_paths

def get_audio(idx, audios_paths, silence=True):
    """获得音频"""
    audio_effect_path = "public/audio_effects"
    audio = mp.AudioFileClip(audios_paths[idx])
    # if silence:
    # audio = audio.subclip(0, audio.duration - 0.5)  # 去掉最后几秒的停顿
    # silence_audio = mp.AudioFileClip(
    #     r"public\blank_audio.m4a").subclip(0, 0.5)
    # audio = mp.concatenate_audioclips([audio, silence_audio])
    # else:
    #     silence_audio = mp.AudioFileClip(
    #         r"public\blank_audio.m4a").subclip(0, 0.3)
    #     audio = mp.concatenate_audioclips([audio, silence_audio])
    if random.random() > 0.6:
        effect = os.path.join(audio_effect_path, random.choice(os.listdir(audio_effect_path)))
        effect = mp.AudioFileClip(effect).volumex(0.05).set_start(random.randint(0, int(audio.duration)))
        audio = mp.CompositeAudioClip([audio, effect])
    return audio


def get_random_font(font_dir):
    fonts = os.listdir(font_dir)
    fonts.remove("README.md")
    return font_dir + "/" + random.choice(fonts)


def get_subtitle(text, color, duration, screen_height, font=None, fontsize=60, stroke_width=1.5, text_length=9):
    if not font:
        current_font = get_random_font(FONT_DIR)
    else:
        current_font = font
    current_font = current_font.replace("\\", "/")
    split_text = merge_strings(re.split('([' + punctuation + '])', text), text_length)
    script_text = get_script(split_text)
    if color == 'white':
        stroke_color = 'black'
    else:
        stroke_color = 'white'
    subtitle = mp.TextClip(script_text, fontsize=fontsize, color=color, font=current_font,
                           stroke_color=stroke_color, stroke_width=stroke_width)
    subtitle = subtitle.set_duration(duration).set_position(('center', 12 / 16 * screen_height))
    return script_text, subtitle

def get_cdn_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        # 将图片数据加载到内存
        image_data = io.BytesIO(response.content)
        image = Image.open(image_data)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = np.array(image)

        return image
    else:
        print("图片下载失败")
        return ""

def get_cdn_video(video_url):
    response = requests.get(video_url)
    if response.status_code == 200:
        video_data = io.BytesIO(response.content)

        # 将视频数据保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            tmpfile.write(video_data.read())
            temp_video_path = tmpfile.name

        # 使用 moviepy 读取临时文件
        clip = mp.VideoFileClip(temp_video_path)
        return clip

def concat_audios(audio_path, bitrate="192k"):
    # 初始化一个空的音频段
    combined = AudioSegment.empty()

    # 遍历指定目录下的所有文件
    for filename in os.listdir(audio_path):
        # 检查文件是否为 MP3 文件
        if filename.endswith('.mp3'):
            # 加载音频文件
            sound = AudioSegment.from_file(os.path.join(audio_path, filename), format="mp3")
            # 将当前音频文件追加到合并音频中
            combined += sound

    # 导出合并后的音频
    path = audio_path + ".mp3"
    combined.export(path, format="mp3", bitrate=bitrate)
    return path

def generate_video(background_pic, script_texts, material_list, voice_name, color, bg_music_path, express, font):
    video_start = time.time()
    update_current_project_progress(1.0)
    video_name = os.path.join("db", "video", f"output_video_{time.time()}_{random.random()}.mp4")

    #### 人声音频 TODO: 修改音频的名字(太短了)
    if "zh-CN" in voice_name:
        audio_path, audios_paths = generate_ms_audio(voice_name, script_texts, express)
        silence = True
    else:
        audio_path, audios_paths = generate_my_audio(voice_name, script_texts, express)
        silence = False
    full_audio_path = concat_audios(audio_path)

    #### 背景
    background = mp.ImageClip(background_pic)
    screen_width, screen_height = background.size


    all_audios = []  # 记录用过的素材
    all_videos = []
    update_current_project_progress(10.0)       # TODO: 加上多线程
    for idx, material in enumerate(material_list):
        walk_progress = idx / len(material_list)
        update_current_project_progress(round(10 + walk_progress * 40, 2))
        print(f"\t开始拼接第 {idx + 1} 个片段！", end="\t")

        #### 音频和背景
        audio = get_audio(idx, audios_paths, silence=silence)

        #### 字幕
        script_text, subtitle = get_subtitle(script_texts[idx], color, audio.duration, screen_height, font)

        #### 素材
        image_path, ends = material[0], material[1]
        if ends in ["image"]:
            image = get_cdn_image(image_path)
            image = mp.ImageClip(image)
            image = image.set_duration(audio.duration)
            image = transition(image, audio, DESIRED_HEIGHT, background.size[0])
            # 不能随便清理视频、音频，不然会乱！
        elif ends in ["video"]:
            image = get_cdn_video(image_path)
            video_clip = image.set_audio(None)
            if video_clip.duration < audio.duration:
                copied_clip = video_clip.copy()
                video_clip = mp.concatenate_videoclips([video_clip, copied_clip])
            start2 = max(0, random.uniform(0, video_clip.duration - audio.duration - 0.5))
            video_clip = video_clip.subclip(start2, audio.duration + start2)
            video_clip = transition(video_clip,
                                    audio, DESIRED_HEIGHT, background.size[0], is_video=True)
            image = video_clip.set_position('center').resize(width=background.size[0])
        else:
            print(f"{ends} 这个格式不对！请注意程序报错！")


        ### 合成视频
        temp_background = background.set_duration(audio.duration)
        com_video = mp.CompositeVideoClip([temp_background, image, subtitle]).set_duration(audio.duration)  # 优化递归！

        all_videos.append(com_video)
        all_audios.append(audio)
        print("图片大小为：", image.size,
              f"视频长度：{image.duration}；音频长度：{audio.duration}",
              f"背景长度：{temp_background.duration}",
              f"字幕长度：{subtitle.duration}",
              f"导出视频长度：{com_video.duration}", end="\n")
    full_video = mp.concatenate_videoclips(all_videos)
    full_audio = mp.AudioFileClip(full_audio_path)
    full_video = full_video.set_audio(full_audio)

    #### 背景音乐
    while True:
        try:
            bg_music = mp.AudioFileClip(bg_music_path)
            bg_music = mp.concatenate_audioclips([bg_music, bg_music, bg_music])
            print(f"音乐长度为：{bg_music.duration} 秒")
            break
        except:     # TODO: 如果音乐报错了怎么办？
            print("音乐选择出了问题！")
    bg_music = bg_music.volumex(0.08).set_duration(full_video.duration)
    voice_audio = full_video.audio
    combined_audio = mp.CompositeAudioClip([voice_audio, bg_music])
    full_video = full_video.set_audio(combined_audio)

    #### 导出视频
    times = 2
    while times:
        try:
            full_video.memoize = False
            start = time.time()
            full_video.write_videofile(video_name, fps=FPS, threads="auto", codec='h264_nvenc', audio_codec='aac')
            print(f"视频导出成功！花费时间为 {time.time() - start} 秒")
            url = upload_output_video(video_name)
            update_current_project_progress(100)
            break
        except Exception as e:
            if times <= 0:
                return "error"
            print(f"内存不够了！{e}")
            time.sleep(5)
            times -= 1

    background.close()
    audio.close()
    subtitle.close()
    # image.close()
    com_video.close()
    full_video.close()
    bg_music.close()
    combined_audio.close()
    del background
    del audio
    del subtitle
    del com_video
    del full_video
    del bg_music
    del combined_audio
    try:
        image.close()
        del image
    except:
        video_clip.close()
        del video_clip
    gc.collect()

    return url