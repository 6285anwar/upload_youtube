import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import requests
import cv2
import time
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import time
import shutil

import datetime

time_slots = {
    1: "02:30:00",
    2: "05:30:00",
    3: "08:30:00",
    4: "11:30:00",
    5: "14:30:00",
}

youtube_video_titile = []
youtube_video_description = []
video_ids = []


def success():
    time.sleep(60)
    print("================== | video Uploaded | ==================")


def upload_video_to_youtube():
    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")
    folder_path =  "C:/Users/New/AppData/Local/Programs/Python/Amazone"
    youtube_video_titile_out = ' '.join(youtube_video_titile)
    youtube_video_description_out = ' '.join(youtube_video_description)
    for file_name in os.listdir(folder_path):
        if file_name.startswith('output') and file_name.endswith('.mp4'):
            current_time = datetime.datetime.now().time()
            print(current_time)
            next_time = None
            for i in range(1, 6):
                if datetime.datetime.strptime(time_slots[i], "%H:%M:%S").time() > current_time:
                    next_time = datetime.datetime.strptime(time_slots[i], "%H:%M:%S").time()
                    break

            if not next_time:
                # no more time periods today, set next_time to first time slot of next day
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                next_time = datetime.datetime.strptime(time_slots[1], "%H:%M:%S").time()
                time_diff = datetime.datetime.combine(tomorrow.date(), next_time) - datetime.datetime.now()
            else:
                # time period found, calculate time difference
                time_diff = datetime.datetime.combine(datetime.date.today(), next_time) - datetime.datetime.combine(datetime.date.today(), current_time)

            print("Next time period:", next_time)
            print("Waiting for:", time_diff)

            time.sleep(time_diff.seconds)
            video_path = os.path.join(folder_path, file_name)
            video = LocalVideo(file_path=video_path)
            video.set_title(youtube_video_titile_out)
            video.set_description(youtube_video_description_out)
            video.set_tags(["tag1", "tag2", "tag3"])
            video.set_default_language("en-US")
            video.set_embeddable(True)
            video.set_license("creativeCommon")    
            video.set_privacy_status("public")
            video.set_public_stats_viewable(True)
            video = channel.upload_video(video)
            video_ids.append(video.id)
            print(f"Video uploaded successfully. ID: {video.id}")

            success()






















# def upload_video_to_youtube():
#     channel = Channel()
#     channel.login("client_secrets.json", "credentials.storage")
#     folder_path =  "C:/Users/New/AppData/Local/Programs/Python/Amazone"
#     youtube_video_titile_out = ' '.join(youtube_video_titile)
#     youtube_video_description_out = ' '.join(youtube_video_description)
#     for file_name in os.listdir(folder_path):
#         if file_name.startswith('output') and file_name.endswith('.mp4'):

#             if len(video_ids) >= 5:
#                 print("Waiting for 24 hours before uploading more videos...")
#                 time.sleep(86400)
#                 video_ids.clear()

#             video_path = os.path.join(folder_path, file_name)
#             video = LocalVideo(file_path=video_path)
#             video.set_title(youtube_video_titile_out)
#             video.set_description(youtube_video_description_out)
#             video.set_tags(["tag1", "tag2", "tag3"])
#             video.set_default_language("en-US")
#             video.set_embeddable(True)
#             video.set_license("creativeCommon")    
#             video.set_privacy_status("unlisted")
#             video.set_public_stats_viewable(True)
#             scheduled_time = datetime.datetime(2023,4,1,0,0,0)
#             video.set_publish_at(scheduled_time)
#             video = channel.upload_video(video)
#             video_ids.append(video.id)
#             print(f"Video uploaded successfully. ID: {video.id}")

#             success()




# def upload_video_to_youtube():
#     folder_path = "C:/Users/New/AppData/Local/Programs/Python/Amazone"
#     files = os.listdir(folder_path)
#     print(video_ids)
#     for file in files:
#         print("file")
#         if file.endswith('.mp4'):
#             channel = Channel()
#             channel.login("client_secrets.json", "credentials.storage")
#             mainvedio = file
#             youtube_video_titile_out = ' '.join(youtube_video_titile)
#             youtube_video_description_out = ' '.join(youtube_video_description)

#             title= youtube_video_titile_out
#             descr= youtube_video_description_out
#             video = LocalVideo(file_path= mainvedio)
#             # setting snippet
#             video.set_title(title)
#             video.set_description(descr)
#             video.set_tags(["this", "tag"])
#             video.set_default_language("en-US")
#             print("video snippit")
#             # setting status
#             video.set_embeddable(True)
#             video.set_license("creativeCommon")
#             video.set_privacy_status("public")
#             video.set_public_stats_viewable(True)
#             print("video status")

#             video = channel.upload_video(video)

#             print("uploading................................................................................")
#             video_ids.append(video.id)
#             if len(video_ids) >= 5:
#                     print("Waiting for 24 hours before uploading more videos...")
#                     time.sleep(86400)  
#                     video_ids.clear()

#             print(video.id)
#             print(video)

#             # liking video
#             video.like()
#     success()

def video_length_cutter():
    video_cutter = VideoFileClip("Product_Video_frame_watermark.mp4")
    duration = video_cutter.duration

    if duration <= 60:
        video_cutter.close()  
        os.rename("Product_Video_frame_watermark.mp4","output1.mp4")

    elif duration <= 120:
        half_duration = duration / 2
        clip1 = video_cutter.subclip(0, half_duration)
        clip2 = video_cutter.subclip(half_duration, duration)
        clip1.write_videofile("output1.mp4")
        clip2.write_videofile("output2.mp4")
    else:
        num_clips = int(duration / 60)
        remainder = duration % 60
        clips = []
        for i in range(num_clips - 1):
            start = i * 60
            end = (i + 1) * 60
            clip = video_cutter.subclip(start, end)
            clip.write_videofile(f"output{i}.mp4")
        if remainder < 60:
            start = (num_clips - 1) * 60
            end = (((num_clips - 1) * 60) - duration) / 2
            clip1 = video_cutter.subclip(start, end)
            clip2 = video_cutter.subclip(end, duration)
            clip1.write_videofile(f"output{i+1}.mp4")
            clip2.write_videofile(f"output{i+2}.mp4")
        else:
            start = (num_clips - 1) * 60
            end = num_clips * 60
            clip = video_cutter.subclip(start, end)
            clip.write_videofile(f"output{num_clips - 1}.mp4")
    
    print("=========================== | video Cutted | =====================")
    upload_video_to_youtube()

def video_cutt_logo():
    video_clip = VideoFileClip("Product_Video.mp4")
    audio_clip = video_clip.audio
    video_clip = video_clip.without_audio()
    audio_clip.write_audiofile("my_audio.mp3")
    video_clip.write_videofile("my_video_no_audio.mp4")
    audio_clip.close()
    video_clip.close()

    cap = cv2.VideoCapture('my_video_no_audio.mp4')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    aspect_ratio = width / height
    new_height = int(width)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('ratiooutput_video.mp4', fourcc, 30, (width, new_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            top_bar = int((new_height - height) / 2)
            bottom_bar = new_height - height - top_bar
            frame = cv2.copyMakeBorder(frame, top_bar, bottom_bar, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            out.write(frame)
        else:
            break

    cap.release()
    out.release()

    video_clip = VideoFileClip('ratiooutput_video.mp4')
    audio_clip = AudioFileClip('my_audio.mp3')
    audio_clip = audio_clip.set_duration(video_clip.duration)
    final_clip = CompositeVideoClip([video_clip]).set_audio(audio_clip)
    final_clip.write_videofile('my_final_video.mp4')
    video_clip.close()
    audio_clip.close()
    final_clip.close()

    video_clip = VideoFileClip('my_final_video.mp4')
    video_duration = video_clip.duration
    top_image = ImageClip('buylink0.png').set_position(('center', 'top')).resize(1.2)
    bottom_image = ImageClip('buylink0.png').set_position(('center', 'bottom')).resize(1.2)
    watermark = ImageClip('atoz.png').set_opacity(0.3).set_position(('center', 450)).resize(0.3)
    composite_clip = CompositeVideoClip([video_clip, bottom_image, watermark,top_image])
    composite_clip.duration = video_clip.duration
    composite_clip.write_videofile('Product_Video_frame_watermark.mp4', fps=video_clip.fps)

    video_length_cutter()


def video_scraping():
    urls = ["https://www.amazon.in/gp/bestsellers/automotive/?ie=UTF8&ref_=sv_automotivesubnav_1",
            "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_pg_1?ie=UTF8&pg=1",
            "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_pg_2?ie=UTF8&pg=2",
            "https://www.amazon.in/gp/bestsellers/automotive/5257472031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257473031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257474031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257475031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257476031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257477031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257478031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257480031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257481031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257482031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257483031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257484031/ref=zg_bs_nav_automotive_1",
            "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_unv_automotive_1_5257475031_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257472031/ref=zg_bs_pg_1?ie=UTF8&pg=1",
            "https://www.amazon.in/gp/bestsellers/automotive/5257472031/ref=zg_bs_pg_2?ie=UTF8&pg=2",
            "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_unv_automotive_1_5257472031_1",
            "https://www.amazon.in/gp/bestsellers/automotive/5361935031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257487031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257488031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257497031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257489031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257490031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257491031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257492031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257493031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257494031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257495031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257496031/ref=zg_bs_nav_automotive_2_5257472031",
            "https://www.amazon.in/gp/bestsellers/automotive/28127475031/ref=zg_bs_nav_automotive_3_5257487031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257641031/ref=zg_bs_nav_automotive_4_28127475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257642031/ref=zg_bs_nav_automotive_4_5257641031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257643031/ref=zg_bs_nav_automotive_4_5257642031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257672031/ref=zg_bs_nav_automotive_3_5257497031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348313031/ref=zg_bs_nav_automotive_3_5257672031",
            "https://www.amazon.in/gp/bestsellers/automotive/28127476031/ref=zg_bs_nav_automotive_3_51348313031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257673031/ref=zg_bs_nav_automotive_3_28127476031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257674031/ref=zg_bs_nav_automotive_3_5257673031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257649031/ref=zg_bs_nav_automotive_3_5257490031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257646031/ref=zg_bs_nav_automotive_3_5257649031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257648031/ref=zg_bs_nav_automotive_3_5257646031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257647031/ref=zg_bs_nav_automotive_3_5257648031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257655031/ref=zg_bs_nav_automotive_3_5257491031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257656031/ref=zg_bs_nav_automotive_3_5257655031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257658031/ref=zg_bs_nav_automotive_3_5257656031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257660031/ref=zg_bs_nav_automotive_3_5257658031",
            "https://www.amazon.in/gp/bestsellers/automotive/2083413031/ref=zg_bs_nav_automotive_3_5257660031",
            "https://www.amazon.in/gp/bestsellers/automotive/28127479031/ref=zg_bs_nav_automotive_4_28127478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257654031/ref=zg_bs_nav_automotive_3_5257491031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257663031/ref=zg_bs_nav_automotive_3_5257662031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257665031/ref=zg_bs_nav_automotive_3_5257663031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257495031/ref=zg_bs_nav_automotive_2_5257494031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257666031/ref=zg_bs_nav_automotive_3_5257495031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257667031/ref=zg_bs_nav_automotive_3_5257666031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348354031/ref=zg_bs_nav_automotive_4_5257667031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348355031/ref=zg_bs_nav_automotive_4_51348354031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348315031/ref=zg_bs_nav_automotive_3_5257666031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257668031/ref=zg_bs_nav_automotive_3_5257666031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257669031/ref=zg_bs_nav_automotive_3_5257496031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257670031/ref=zg_bs_nav_automotive_3_5257669031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389228031/ref=zg_bs_nav_electronics_4_1389227031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389229031/ref=zg_bs_nav_electronics_4_1389228031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389230031/ref=zg_bs_nav_electronics_4_1389229031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389232031/ref=zg_bs_nav_electronics_5_1389231031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389234031/ref=zg_bs_nav_electronics_5_1389232031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389235031/ref=zg_bs_nav_electronics_5_1389234031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389237031/ref=zg_bs_nav_electronics_5_1389235031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389239031/ref=zg_bs_nav_electronics_5_1389237031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389241031/ref=zg_bs_nav_electronics_5_1389239031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389242031/ref=zg_bs_nav_electronics_5_1389241031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389243031/ref=zg_bs_nav_electronics_5_1389242031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389245031/ref=zg_bs_nav_electronics_5_1389243031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389246031/ref=zg_bs_nav_electronics_5_1389245031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389248031/ref=zg_bs_nav_electronics_5_1389246031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389249031/ref=zg_bs_nav_electronics_5_1389248031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389255031/ref=zg_bs_nav_electronics_5_1389249031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389257031/ref=zg_bs_nav_electronics_5_51419995031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389258031/ref=zg_bs_nav_electronics_4_1389230031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389259031/ref=zg_bs_nav_electronics_4_1389258031",
            "https://www.amazon.in/gp/bestsellers/electronics/1592753031/ref=zg_bs_nav_electronics_4_1389259031",
            "https://www.amazon.in/gp/bestsellers/electronics/1592754031/ref=zg_bs_nav_electronics_4_1592753031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419960031/ref=zg_bs_nav_electronics_4_1592754031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389260031/ref=zg_bs_nav_electronics_4_51419960031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389261031/ref=zg_bs_nav_electronics_4_1389260031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389262031/ref=zg_bs_nav_electronics_4_1389261031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389264031/ref=zg_bs_nav_electronics_3_1389226031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389321031/ref=zg_bs_nav_electronics_4_1389264031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389323031/ref=zg_bs_nav_electronics_3_1389321031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389325031/ref=zg_bs_nav_electronics_3_1389323031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389406031/ref=zg_bs_nav_electronics_3_1389226031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389411031/ref=zg_bs_nav_electronics_4_1389406031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389407031/ref=zg_bs_nav_electronics_4_1389411031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389408031/ref=zg_bs_nav_electronics_4_1389407031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389267031/ref=zg_bs_nav_automotive_2_5257473031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389269031/ref=zg_bs_nav_electronics_4_1389268031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389270031/ref=zg_bs_nav_electronics_5_1389269031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389271031/ref=zg_bs_nav_electronics_5_1389270031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389272031/ref=zg_bs_nav_electronics_5_1389271031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389274031/ref=zg_bs_nav_electronics_4_1389273031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389275031/ref=zg_bs_nav_electronics_4_1389274031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389276031/ref=zg_bs_nav_electronics_4_1389275031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389278031/ref=zg_bs_nav_electronics_5_1389277031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389279031/ref=zg_bs_nav_electronics_5_1389278031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419996031/ref=zg_bs_nav_electronics_5_1389279031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389280031/ref=zg_bs_nav_electronics_5_51419996031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389291031/ref=zg_bs_nav_electronics_4_1389290031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419963031/ref=zg_bs_nav_electronics_4_1389291031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419910031/ref=zg_bs_nav_electronics_3_1389267031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419909031/ref=zg_bs_nav_electronics_3_51419910031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389310031/ref=zg_bs_nav_automotive_2_5257473031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389311031/ref=zg_bs_nav_electronics_3_1389310031",
            "https://www.amazon.in/gp/bestsellers/electronics/1592753031/ref=zg_bs_nav_electronics_3_1389311031",
            "https://www.amazon.in/gp/bestsellers/electronics/1389313031/ref=zg_bs_nav_electronics_3_1389311031",
            "https://www.amazon.in/gp/bestsellers/electronics/1592754031/ref=zg_bs_nav_electronics_3_1389313031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419913031/ref=zg_bs_nav_electronics_3_1389313031",
            "https://www.amazon.in/gp/bestsellers/automotive/27366197031/ref=zg_bs_nav_automotive_4_5257509031",
            "https://www.amazon.in/gp/bestsellers/automotive/27366198031/ref=zg_bs_nav_automotive_4_27366197031",
            "https://www.amazon.in/gp/bestsellers/automotive/27366199031/ref=zg_bs_nav_automotive_4_27366198031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257501031/ref=zg_bs_nav_automotive_3_15439785031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257677031/ref=zg_bs_nav_automotive_4_5257501031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348350031/ref=zg_bs_nav_automotive_4_5257677031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257502031/ref=zg_bs_nav_automotive_3_15439785031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348352031/ref=zg_bs_nav_automotive_4_5257502031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348351031/ref=zg_bs_nav_automotive_4_51348352031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257508031/ref=zg_bs_nav_automotive_3_15439785031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348300031/ref=zg_bs_nav_automotive_3_15439785031",
            "https://www.amazon.in/gp/bestsellers/automotive/10279698031/ref=zg_bs_nav_automotive_3_51348300031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257511031/ref=zg_bs_nav_automotive_3_10279698031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257512031/ref=zg_bs_nav_automotive_3_5257511031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257516031/ref=zg_bs_nav_automotive_3_5257512031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257514031/ref=zg_bs_nav_automotive_3_5257516031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257654031/ref=zg_bs_nav_automotive_3_5257514031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348349031/ref=zg_bs_nav_automotive_4_5257522031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348346031/ref=zg_bs_nav_automotive_4_51348349031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348347031/ref=zg_bs_nav_automotive_4_51348346031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348348031/ref=zg_bs_nav_automotive_4_51348347031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257554031/ref=zg_bs_nav_automotive_3_5257514031",
            "https://www.amazon.in/gp/bestsellers/automotive/27019335031/ref=zg_bs_nav_automotive_4_5257554031",
            "https://www.amazon.in/gp/bestsellers/automotive/27019334031/ref=zg_bs_nav_automotive_4_27019335031",
            "https://www.amazon.in/gp/bestsellers/automotive/27019336031/ref=zg_bs_nav_automotive_4_27019334031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389259031/ref=zg_bs_nav_automotive_2_5257474031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257498031/ref=zg_bs_nav_automotive_3_15439784031",
            "https://www.amazon.in/gp/bestsellers/automotive/10279697031/ref=zg_bs_nav_automotive_3_5257498031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257499031/ref=zg_bs_nav_automotive_3_10279697031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257500031/ref=zg_bs_nav_automotive_3_5257499031",
            "https://www.amazon.in/gp/bestsellers/automotive/52296795031/ref=zg_bs_nav_automotive_3_5257500031",
            "https://www.amazon.in/gp/bestsellers/automotive/66059950031/ref=zg_bs_nav_automotive_3_52296795031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257699031/ref=zg_bs_nav_automotive_4_5257518031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257518031/ref=zg_bs_nav_automotive_3_66059950031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257697031/ref=zg_bs_nav_automotive_4_5257518031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348345031/ref=zg_bs_nav_automotive_4_5257697031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348341031/ref=zg_bs_nav_automotive_4_51348345031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257698031/ref=zg_bs_nav_automotive_4_51348341031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348344031/ref=zg_bs_nav_automotive_4_5257698031",
            "https://www.amazon.in/gp/bestsellers/automotive/10279699031/ref=zg_bs_nav_automotive_4_51348344031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348342031/ref=zg_bs_nav_automotive_4_10279699031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348343031/ref=zg_bs_nav_automotive_4_51348342031",
            "https://www.amazon.in/gp/bestsellers/automotive/5816261031/ref=zg_bs_nav_automotive_3_66059950031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257748031/ref=zg_bs_nav_automotive_3_5816261031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257506031/ref=zg_bs_nav_automotive_3_5257748031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348298031/ref=zg_bs_nav_automotive_3_5257506031",
            "https://www.amazon.in/gp/bestsellers/automotive/26286457031/ref=zg_bs_nav_automotive_3_51348298031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257510031/ref=zg_bs_nav_automotive_3_26286457031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257689031/ref=zg_bs_nav_automotive_4_5257510031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257690031/ref=zg_bs_nav_automotive_4_5257689031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257691031/ref=zg_bs_nav_automotive_4_5257690031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257513031/ref=zg_bs_nav_automotive_3_26286457031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348299031/ref=zg_bs_nav_automotive_3_5257513031",
            "https://www.amazon.in/gp/bestsellers/automotive/26286457031/ref=zg_bs_nav_automotive_4_5257517031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257517031/ref=zg_bs_nav_automotive_3_51348299031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257694031/ref=zg_bs_nav_automotive_4_5257517031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257692031/ref=zg_bs_nav_automotive_4_5257694031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257695031/ref=zg_bs_nav_automotive_4_5257692031",
            "https://www.amazon.in/gp/bestsellers/automotive/10279696031/ref=zg_bs_nav_automotive_3_51348299031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258293031/ref=zg_bs_nav_automotive_4_10279696031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258295031/ref=zg_bs_nav_automotive_4_5258293031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257520031/ref=zg_bs_nav_automotive_3_51348299031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257701031/ref=zg_bs_nav_automotive_4_5257520031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257702031/ref=zg_bs_nav_automotive_4_5257701031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257703031/ref=zg_bs_nav_automotive_4_5257702031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257521031/ref=zg_bs_nav_automotive_3_51348299031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257527031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257712031/ref=zg_bs_nav_automotive_3_5257527031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348270031/ref=zg_bs_nav_automotive_3_5257712031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257713031/ref=zg_bs_nav_automotive_3_51348270031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257719031/ref=zg_bs_nav_automotive_3_5257529031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348257031/ref=zg_bs_nav_automotive_3_5257719031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257721031/ref=zg_bs_nav_automotive_3_51348257031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258185031/ref=zg_bs_nav_automotive_4_5257721031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258186031/ref=zg_bs_nav_automotive_4_5258185031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258187031/ref=zg_bs_nav_automotive_4_5258186031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257722031/ref=zg_bs_nav_automotive_3_51348257031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257723031/ref=zg_bs_nav_automotive_3_5257722031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257725031/ref=zg_bs_nav_automotive_3_5257723031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348255031/ref=zg_bs_nav_automotive_3_5257725031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257727031/ref=zg_bs_nav_automotive_3_51348255031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258189031/ref=zg_bs_nav_automotive_4_5257727031",
            "https://www.amazon.in/gp/bestsellers/automotive/14663107031/ref=zg_bs_nav_automotive_4_5258189031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258190031/ref=zg_bs_nav_automotive_4_14663107031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348256031/ref=zg_bs_nav_automotive_3_51348255031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348247031/ref=zg_bs_nav_automotive_3_51348256031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348249031/ref=zg_bs_nav_automotive_3_51348247031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348244031/ref=zg_bs_nav_automotive_3_51348249031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348253031/ref=zg_bs_nav_automotive_3_51348244031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348251031/ref=zg_bs_nav_automotive_3_51348253031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257737031/ref=zg_bs_nav_automotive_3_5257530031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257738031/ref=zg_bs_nav_automotive_3_5257737031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257740031/ref=zg_bs_nav_automotive_3_5257738031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257742031/ref=zg_bs_nav_automotive_3_5257740031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257744031/ref=zg_bs_nav_automotive_3_5257742031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257745031/ref=zg_bs_nav_automotive_3_5257744031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348316031/ref=zg_bs_nav_automotive_4_5257745031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348317031/ref=zg_bs_nav_automotive_4_51348316031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257747031/ref=zg_bs_nav_automotive_3_5257744031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348215031/ref=zg_bs_nav_automotive_3_5257747031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257749031/ref=zg_bs_nav_automotive_3_51348215031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257750031/ref=zg_bs_nav_automotive_3_5257749031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257752031/ref=zg_bs_nav_automotive_3_5257750031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257753031/ref=zg_bs_nav_automotive_3_5257752031",
            "https://www.amazon.in/gp/bestsellers/automotive/27316081031/ref=zg_bs_nav_automotive_3_5257753031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257754031/ref=zg_bs_nav_automotive_3_27316081031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257755031/ref=zg_bs_nav_automotive_3_5257754031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257757031/ref=zg_bs_nav_automotive_3_5257755031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258202031/ref=zg_bs_nav_automotive_4_5257757031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258203031/ref=zg_bs_nav_automotive_4_5258202031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258204031/ref=zg_bs_nav_automotive_4_5258203031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258206031/ref=zg_bs_nav_automotive_4_5258205031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257758031/ref=zg_bs_nav_automotive_3_5257755031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257760031/ref=zg_bs_nav_automotive_3_5257758031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348214031/ref=zg_bs_nav_automotive_3_5257760031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348213031/ref=zg_bs_nav_automotive_3_51348214031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257762031/ref=zg_bs_nav_automotive_3_51348213031",
            "https://www.amazon.in/gp/bestsellers/automotive/28127474031/ref=zg_bs_nav_automotive_3_5257762031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257764031/ref=zg_bs_nav_automotive_3_28127474031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258213031/ref=zg_bs_nav_automotive_4_5257764031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258214031/ref=zg_bs_nav_automotive_4_5258213031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258215031/ref=zg_bs_nav_automotive_4_5258214031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258216031/ref=zg_bs_nav_automotive_4_5258215031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257531031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257765031/ref=zg_bs_nav_automotive_3_5257531031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257766031/ref=zg_bs_nav_automotive_3_5257765031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348326031/ref=zg_bs_nav_automotive_4_5257766031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258217031/ref=zg_bs_nav_automotive_4_51348326031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258223031/ref=zg_bs_nav_automotive_4_5258217031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258225031/ref=zg_bs_nav_automotive_4_5258223031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348325031/ref=zg_bs_nav_automotive_4_5258225031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257768031/ref=zg_bs_nav_automotive_3_5257765031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348323031/ref=zg_bs_nav_automotive_4_5257768031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348324031/ref=zg_bs_nav_automotive_4_51348323031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348268031/ref=zg_bs_nav_automotive_3_5257765031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348266031/ref=zg_bs_nav_automotive_3_51348268031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257532031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257770031/ref=zg_bs_nav_automotive_3_5257532031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257773031/ref=zg_bs_nav_automotive_3_5257770031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257774031/ref=zg_bs_nav_automotive_3_5257773031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257776031/ref=zg_bs_nav_automotive_3_5257774031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348318031/ref=zg_bs_nav_automotive_4_5257776031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257533031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348237031/ref=zg_bs_nav_automotive_3_5257533031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348236031/ref=zg_bs_nav_automotive_3_51348237031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348238031/ref=zg_bs_nav_automotive_3_51348236031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348240031/ref=zg_bs_nav_automotive_3_51348238031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348239031/ref=zg_bs_nav_automotive_3_51348240031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348242031/ref=zg_bs_nav_automotive_3_51348239031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348241031/ref=zg_bs_nav_automotive_3_51348242031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257534031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257794031/ref=zg_bs_nav_automotive_3_5257534031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258287031/ref=zg_bs_nav_automotive_4_5257794031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258288031/ref=zg_bs_nav_automotive_4_5258287031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257795031/ref=zg_bs_nav_automotive_3_5257534031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348258031/ref=zg_bs_nav_automotive_3_5257795031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257796031/ref=zg_bs_nav_automotive_3_51348258031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257797031/ref=zg_bs_nav_automotive_3_5257796031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257798031/ref=zg_bs_nav_automotive_3_5257797031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257535031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257800031/ref=zg_bs_nav_automotive_3_5257535031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257801031/ref=zg_bs_nav_automotive_3_5257800031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257536031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348260031/ref=zg_bs_nav_automotive_3_5257536031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257803031/ref=zg_bs_nav_automotive_3_51348260031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257806031/ref=zg_bs_nav_automotive_3_5257803031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257537031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348196031/ref=zg_bs_nav_automotive_3_5257537031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348201031/ref=zg_bs_nav_automotive_3_51348196031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348206031/ref=zg_bs_nav_automotive_3_51348201031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348205031/ref=zg_bs_nav_automotive_3_51348206031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348202031/ref=zg_bs_nav_automotive_3_51348205031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348203031/ref=zg_bs_nav_automotive_3_51348202031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348200031/ref=zg_bs_nav_automotive_3_51348203031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348207031/ref=zg_bs_nav_automotive_3_51348200031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348198031/ref=zg_bs_nav_automotive_3_51348199031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348204031/ref=zg_bs_nav_automotive_3_51348198031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257814031/ref=zg_bs_nav_automotive_3_51348204031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348197031/ref=zg_bs_nav_automotive_3_5257814031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348208031/ref=zg_bs_nav_automotive_3_51348197031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348209031/ref=zg_bs_nav_automotive_3_51348208031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257538031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257819031/ref=zg_bs_nav_automotive_3_5257818031",
            "https://www.amazon.in/gp/bestsellers/automotive/27231724031/ref=zg_bs_nav_automotive_3_5257819031",
            "https://www.amazon.in/gp/bestsellers/automotive/27231725031/ref=zg_bs_nav_automotive_4_27231724031",
            "https://www.amazon.in/gp/bestsellers/automotive/27231726031/ref=zg_bs_nav_automotive_4_27231725031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257817031/ref=zg_bs_nav_automotive_4_27231726031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257821031/ref=zg_bs_nav_automotive_3_5257819031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257822031/ref=zg_bs_nav_automotive_3_5257821031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257824031/ref=zg_bs_nav_automotive_3_5257822031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257825031/ref=zg_bs_nav_automotive_3_5257824031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257826031/ref=zg_bs_nav_automotive_3_5257825031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257828031/ref=zg_bs_nav_automotive_3_5257826031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257829031/ref=zg_bs_nav_automotive_3_5257828031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348212031/ref=zg_bs_nav_automotive_3_5257829031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257831031/ref=zg_bs_nav_automotive_3_51348212031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257832031/ref=zg_bs_nav_automotive_3_5257831031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257834031/ref=zg_bs_nav_automotive_3_5257832031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348210031/ref=zg_bs_nav_automotive_3_5257834031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257838031/ref=zg_bs_nav_automotive_3_51348210031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257840031/ref=zg_bs_nav_automotive_3_5257838031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258290031/ref=zg_bs_nav_automotive_4_5257840031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257842031/ref=zg_bs_nav_automotive_3_5257838031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258293031/ref=zg_bs_nav_automotive_4_5257842031",
            "https://www.amazon.in/gp/bestsellers/automotive/10279696031/ref=zg_bs_nav_automotive_4_5258293031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258295031/ref=zg_bs_nav_automotive_4_10279696031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257843031/ref=zg_bs_nav_automotive_3_5257838031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257844031/ref=zg_bs_nav_automotive_3_5257843031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348211031/ref=zg_bs_nav_automotive_3_5257844031",
            "https://www.amazon.in/gp/bestsellers/automotive/28127474031/ref=zg_bs_nav_automotive_3_51348211031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257539031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/27316221031/ref=zg_bs_nav_automotive_3_5257539031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257846031/ref=zg_bs_nav_automotive_4_27316221031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348262031/ref=zg_bs_nav_automotive_3_5257539031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257847031/ref=zg_bs_nav_automotive_3_51348262031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258296031/ref=zg_bs_nav_automotive_4_5257847031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348365031/ref=zg_bs_nav_automotive_5_5258296031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348361031/ref=zg_bs_nav_automotive_5_51348365031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348360031/ref=zg_bs_nav_automotive_5_51348361031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348358031/ref=zg_bs_nav_automotive_5_51348360031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348356031/ref=zg_bs_nav_automotive_5_51348358031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348357031/ref=zg_bs_nav_automotive_5_51348356031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348359031/ref=zg_bs_nav_automotive_5_51348357031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348363031/ref=zg_bs_nav_automotive_5_51348359031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348362031/ref=zg_bs_nav_automotive_5_51348363031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348364031/ref=zg_bs_nav_automotive_5_51348362031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258297031/ref=zg_bs_nav_automotive_4_5257847031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348369031/ref=zg_bs_nav_automotive_5_5258297031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258528031/ref=zg_bs_nav_automotive_5_51348369031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348368031/ref=zg_bs_nav_automotive_5_5258528031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348367031/ref=zg_bs_nav_automotive_5_51348368031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258530031/ref=zg_bs_nav_automotive_5_51348367031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348366031/ref=zg_bs_nav_automotive_5_5258530031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348319031/ref=zg_bs_nav_automotive_4_5257847031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258298031/ref=zg_bs_nav_automotive_4_51348319031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258299031/ref=zg_bs_nav_automotive_4_5258298031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257848031/ref=zg_bs_nav_automotive_3_51348262031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258300031/ref=zg_bs_nav_automotive_4_5257848031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258301031/ref=zg_bs_nav_automotive_4_5258300031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348371031/ref=zg_bs_nav_automotive_5_5258301031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258302031/ref=zg_bs_nav_automotive_4_5258300031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258303031/ref=zg_bs_nav_automotive_4_5258302031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258304031/ref=zg_bs_nav_automotive_4_5258303031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348370031/ref=zg_bs_nav_automotive_5_5258304031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258533031/ref=zg_bs_nav_automotive_5_51348370031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258539031/ref=zg_bs_nav_automotive_5_5258533031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258305031/ref=zg_bs_nav_automotive_4_5258303031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348322031/ref=zg_bs_nav_automotive_4_5258305031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258307031/ref=zg_bs_nav_automotive_4_51348322031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258309031/ref=zg_bs_nav_automotive_4_5258307031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258311031/ref=zg_bs_nav_automotive_4_5258309031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348321031/ref=zg_bs_nav_automotive_4_5258311031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258312031/ref=zg_bs_nav_automotive_4_51348321031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348320031/ref=zg_bs_nav_automotive_4_5258312031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258313031/ref=zg_bs_nav_automotive_4_51348320031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348373031/ref=zg_bs_nav_automotive_5_5258313031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348374031/ref=zg_bs_nav_automotive_5_51348373031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348372031/ref=zg_bs_nav_automotive_5_51348374031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348264031/ref=zg_bs_nav_automotive_3_51348262031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348189031/ref=zg_bs_nav_automotive_2_5257475031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348231031/ref=zg_bs_nav_automotive_3_5257540031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348222031/ref=zg_bs_nav_automotive_3_51348231031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348228031/ref=zg_bs_nav_automotive_3_51348222031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348220031/ref=zg_bs_nav_automotive_3_51348228031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348229031/ref=zg_bs_nav_automotive_3_51348220031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348221031/ref=zg_bs_nav_automotive_3_51348229031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348230031/ref=zg_bs_nav_automotive_3_51348221031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348224031/ref=zg_bs_nav_automotive_3_51348230031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348232031/ref=zg_bs_nav_automotive_3_51348224031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348223031/ref=zg_bs_nav_automotive_3_51348232031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348234031/ref=zg_bs_nav_automotive_3_51348223031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348235031/ref=zg_bs_nav_automotive_3_51348234031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348226031/ref=zg_bs_nav_automotive_3_51348235031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348225031/ref=zg_bs_nav_automotive_3_51348226031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348227031/ref=zg_bs_nav_automotive_3_51348225031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258201031/ref=zg_bs_nav_automotive_3_51348227031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257542031/ref=zg_bs_nav_automotive_2_51348189031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257850031/ref=zg_bs_nav_automotive_3_5257542031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257851031/ref=zg_bs_nav_automotive_3_5257850031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348219031/ref=zg_bs_nav_automotive_3_5257851031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348216031/ref=zg_bs_nav_automotive_3_51348219031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257853031/ref=zg_bs_nav_automotive_3_51348216031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258315031/ref=zg_bs_nav_automotive_4_5257853031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258318031/ref=zg_bs_nav_automotive_4_5258315031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348217031/ref=zg_bs_nav_automotive_3_51348216031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257867031/ref=zg_bs_nav_automotive_3_51348217031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257868031/ref=zg_bs_nav_automotive_3_5257867031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257871031/ref=zg_bs_nav_automotive_3_5257868031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257872031/ref=zg_bs_nav_automotive_3_5257871031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257873031/ref=zg_bs_nav_automotive_3_5257872031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257874031/ref=zg_bs_nav_automotive_3_5257873031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258333031/ref=zg_bs_nav_automotive_4_5257874031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258334031/ref=zg_bs_nav_automotive_4_5258333031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258335031/ref=zg_bs_nav_automotive_4_5258334031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348218031/ref=zg_bs_nav_automotive_3_5257873031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257875031/ref=zg_bs_nav_automotive_3_51348218031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257544031/ref=zg_bs_nav_automotive_2_51348189031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257878031/ref=zg_bs_nav_automotive_3_5257544031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257879031/ref=zg_bs_nav_automotive_3_5257878031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257880031/ref=zg_bs_nav_automotive_3_5257879031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348272031/ref=zg_bs_nav_automotive_3_5257880031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257881031/ref=zg_bs_nav_automotive_3_51348272031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257883031/ref=zg_bs_nav_automotive_3_5257545031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257884031/ref=zg_bs_nav_automotive_3_5257883031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257885031/ref=zg_bs_nav_automotive_3_5257884031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257887031/ref=zg_bs_nav_automotive_3_5257885031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257889031/ref=zg_bs_nav_automotive_3_5257887031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257893031/ref=zg_bs_nav_automotive_3_5257889031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257894031/ref=zg_bs_nav_automotive_3_5257893031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257895031/ref=zg_bs_nav_automotive_3_5257894031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258358031/ref=zg_bs_nav_automotive_4_5257895031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258360031/ref=zg_bs_nav_automotive_4_5258358031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258361031/ref=zg_bs_nav_automotive_4_5258360031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348301031/ref=zg_bs_nav_automotive_3_5257894031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257546031/ref=zg_bs_nav_automotive_2_5257476031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257492031/ref=zg_bs_nav_automotive_2_5257546031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257662031/ref=zg_bs_nav_automotive_3_5257492031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257548031/ref=zg_bs_nav_automotive_2_5257546031",
            "https://www.amazon.in/gp/bestsellers/automotive/29853986031/ref=zg_bs_nav_automotive_3_5257548031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348302031/ref=zg_bs_nav_automotive_3_29853986031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348303031/ref=zg_bs_nav_automotive_3_51348302031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348304031/ref=zg_bs_nav_automotive_3_51348303031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348306031/ref=zg_bs_nav_automotive_3_51348304031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258059031/ref=zg_bs_nav_automotive_3_51348306031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348340031/ref=zg_bs_nav_automotive_4_5258059031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348338031/ref=zg_bs_nav_automotive_4_51348340031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348339031/ref=zg_bs_nav_automotive_4_51348338031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348305031/ref=zg_bs_nav_automotive_3_51348306031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257549031/ref=zg_bs_nav_automotive_2_5257546031",
            "https://www.amazon.in/gp/bestsellers/automotive/29853985031/ref=zg_bs_nav_automotive_3_5257549031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348307031/ref=zg_bs_nav_automotive_3_29853985031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348308031/ref=zg_bs_nav_automotive_3_51348307031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348311031/ref=zg_bs_nav_automotive_3_51348308031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348310031/ref=zg_bs_nav_automotive_3_51348311031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348312031/ref=zg_bs_nav_automotive_3_51348310031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348309031/ref=zg_bs_nav_automotive_3_51348312031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257550031/ref=zg_bs_nav_automotive_2_5257477031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257899031/ref=zg_bs_nav_automotive_3_5257550031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257900031/ref=zg_bs_nav_automotive_3_5257899031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257905031/ref=zg_bs_nav_automotive_3_5257900031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257910031/ref=zg_bs_nav_automotive_3_5257905031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257551031/ref=zg_bs_nav_automotive_2_5257477031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257552031/ref=zg_bs_nav_automotive_2_5257551031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257555031/ref=zg_bs_nav_automotive_2_5257552031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257556031/ref=zg_bs_nav_automotive_2_5257555031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257557031/ref=zg_bs_nav_automotive_2_5257556031",
            "https://www.amazon.in/gp/bestsellers/automotive/51396100031/ref=zg_bs_nav_automotive_2_5257557031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257560031/ref=zg_bs_nav_automotive_2_5257557031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257561031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348293031/ref=zg_bs_nav_automotive_3_5257561031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257913031/ref=zg_bs_nav_automotive_3_51348293031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257914031/ref=zg_bs_nav_automotive_3_5257913031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257915031/ref=zg_bs_nav_automotive_3_5257914031",
            "https://www.amazon.in/gp/bestsellers/automotive/3404128031/ref=zg_bs_nav_automotive_3_5257915031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348294031/ref=zg_bs_nav_automotive_3_5257915031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257918031/ref=zg_bs_nav_automotive_3_51348294031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257919031/ref=zg_bs_nav_automotive_3_5257918031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257921031/ref=zg_bs_nav_automotive_3_5257919031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257924031/ref=zg_bs_nav_automotive_3_5257921031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257925031/ref=zg_bs_nav_automotive_3_5257924031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348295031/ref=zg_bs_nav_automotive_3_5257925031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257564031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348291031/ref=zg_bs_nav_automotive_3_5257564031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348290031/ref=zg_bs_nav_automotive_3_51348291031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257929031/ref=zg_bs_nav_automotive_3_51348290031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348289031/ref=zg_bs_nav_automotive_3_5257929031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257930031/ref=zg_bs_nav_automotive_3_51348289031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257931031/ref=zg_bs_nav_automotive_3_5257930031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257932031/ref=zg_bs_nav_automotive_3_5257931031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257933031/ref=zg_bs_nav_automotive_3_5257932031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257934031/ref=zg_bs_nav_automotive_3_5257933031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348288031/ref=zg_bs_nav_automotive_3_5257934031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257567031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257957031/ref=zg_bs_nav_automotive_3_5257567031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348286031/ref=zg_bs_nav_automotive_3_5257957031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257958031/ref=zg_bs_nav_automotive_3_51348286031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257961031/ref=zg_bs_nav_automotive_3_5257958031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348337031/ref=zg_bs_nav_automotive_4_5257961031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257969031/ref=zg_bs_nav_automotive_3_5257958031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257967031/ref=zg_bs_nav_automotive_3_5257969031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257965031/ref=zg_bs_nav_automotive_3_5257967031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257568031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257973031/ref=zg_bs_nav_automotive_3_5257568031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257978031/ref=zg_bs_nav_automotive_3_5257973031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348336031/ref=zg_bs_nav_automotive_4_5257978031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257980031/ref=zg_bs_nav_automotive_3_5257973031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257981031/ref=zg_bs_nav_automotive_3_5257980031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257983031/ref=zg_bs_nav_automotive_3_5257981031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257987031/ref=zg_bs_nav_automotive_3_5257983031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257992031/ref=zg_bs_nav_automotive_3_5257987031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257993031/ref=zg_bs_nav_automotive_3_5257992031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257569031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257994031/ref=zg_bs_nav_automotive_3_5257569031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257995031/ref=zg_bs_nav_automotive_3_5257994031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257996031/ref=zg_bs_nav_automotive_3_5257995031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257997031/ref=zg_bs_nav_automotive_3_5257996031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257998031/ref=zg_bs_nav_automotive_3_5257997031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257999031/ref=zg_bs_nav_automotive_3_5257998031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258000031/ref=zg_bs_nav_automotive_3_5257999031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257570031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258001031/ref=zg_bs_nav_automotive_3_5257570031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258003031/ref=zg_bs_nav_automotive_3_5258001031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257571031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258020031/ref=zg_bs_nav_automotive_3_5257571031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258006031/ref=zg_bs_nav_automotive_3_5258020031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348329031/ref=zg_bs_nav_automotive_4_5258006031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348327031/ref=zg_bs_nav_automotive_4_51348329031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348328031/ref=zg_bs_nav_automotive_4_51348327031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258007031/ref=zg_bs_nav_automotive_3_5258020031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348283031/ref=zg_bs_nav_automotive_3_5258007031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258009031/ref=zg_bs_nav_automotive_3_51348283031",
            "https://www.amazon.in/gp/bestsellers/automotive/12492011031/ref=zg_bs_nav_automotive_3_5258009031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258010031/ref=zg_bs_nav_automotive_3_12492011031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258015031/ref=zg_bs_nav_automotive_3_5258010031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348282031/ref=zg_bs_nav_automotive_3_5258015031",
            "https://www.amazon.in/gp/bestsellers/automotive/12492010031/ref=zg_bs_nav_automotive_3_51348282031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258016031/ref=zg_bs_nav_automotive_3_12492010031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258019031/ref=zg_bs_nav_automotive_3_5258016031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348333031/ref=zg_bs_nav_automotive_4_5258019031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348335031/ref=zg_bs_nav_automotive_4_51348333031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348334031/ref=zg_bs_nav_automotive_4_51348335031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258021031/ref=zg_bs_nav_automotive_3_5258016031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258022031/ref=zg_bs_nav_automotive_3_5258021031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258023031/ref=zg_bs_nav_automotive_3_5258022031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257572031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348287031/ref=zg_bs_nav_automotive_3_5257572031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258045031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258389031/ref=zg_bs_nav_automotive_3_5258045031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258390031/ref=zg_bs_nav_automotive_3_5258389031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258391031/ref=zg_bs_nav_automotive_3_5258390031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258392031/ref=zg_bs_nav_automotive_3_5258391031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258393031/ref=zg_bs_nav_automotive_3_5258392031",
            "https://www.amazon.in/gp/bestsellers/automotive/12443961031/ref=zg_bs_nav_automotive_2_5257478031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257574031/ref=zg_bs_nav_automotive_2_12443961031",
            "https://www.amazon.in/gp/bestsellers/automotive/14053341031/ref=zg_bs_nav_automotive_3_5257574031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348285031/ref=zg_bs_nav_automotive_3_14053341031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258038031/ref=zg_bs_nav_automotive_3_51348285031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258370031/ref=zg_bs_nav_automotive_4_5258038031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258371031/ref=zg_bs_nav_automotive_4_5258370031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258372031/ref=zg_bs_nav_automotive_4_5258371031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258039031/ref=zg_bs_nav_automotive_3_51348285031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258040031/ref=zg_bs_nav_automotive_3_5258039031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258377031/ref=zg_bs_nav_automotive_4_5258040031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258379031/ref=zg_bs_nav_automotive_4_5258377031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258380031/ref=zg_bs_nav_automotive_4_5258379031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348284031/ref=zg_bs_nav_automotive_3_14053341031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257575031/ref=zg_bs_nav_automotive_2_12443961031",
            "https://www.amazon.in/gp/bestsellers/automotive/10543752031/ref=zg_bs_nav_automotive_3_5257575031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258384031/ref=zg_bs_nav_automotive_3_10543752031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182177031/ref=zg_bs_nav_automotive_3_5258384031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182178031/ref=zg_bs_nav_automotive_4_27182177031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182182031/ref=zg_bs_nav_automotive_5_27182178031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182181031/ref=zg_bs_nav_automotive_5_27182182031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182179031/ref=zg_bs_nav_automotive_4_27182177031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182183031/ref=zg_bs_nav_automotive_5_27182179031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182184031/ref=zg_bs_nav_automotive_5_27182183031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182185031/ref=zg_bs_nav_automotive_5_27182180031",
            "https://www.amazon.in/gp/bestsellers/automotive/27182186031/ref=zg_bs_nav_automotive_5_27182185031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258041031/ref=zg_bs_nav_automotive_3_5258384031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258042031/ref=zg_bs_nav_automotive_3_5258041031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258043031/ref=zg_bs_nav_automotive_3_5258042031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258386031/ref=zg_bs_nav_automotive_4_5258043031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258387031/ref=zg_bs_nav_automotive_4_5258386031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258388031/ref=zg_bs_nav_automotive_4_5258387031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258044031/ref=zg_bs_nav_automotive_3_10279695031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258046031/ref=zg_bs_nav_automotive_3_5258044031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258048031/ref=zg_bs_nav_automotive_3_5258046031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258050031/ref=zg_bs_nav_automotive_3_5258048031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258396031/ref=zg_bs_nav_automotive_4_5258050031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258397031/ref=zg_bs_nav_automotive_4_5258396031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258053031/ref=zg_bs_nav_automotive_3_5258048031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257576031/ref=zg_bs_nav_automotive_2_12443961031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257563031/ref=zg_bs_nav_automotive_2_5257576031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257578031/ref=zg_bs_nav_automotive_2_5257563031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348292031/ref=zg_bs_nav_automotive_3_5257578031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258058031/ref=zg_bs_nav_automotive_3_51348292031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258059031/ref=zg_bs_nav_automotive_3_5258058031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389328031/ref=zg_bs_nav_automotive_2_5257480031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419927031/ref=zg_bs_nav_electronics_3_1389328031",
            "https://www.amazon.in/gp/bestsellers/electronics/51419930031/ref=zg_bs_nav_electronics_3_51419927031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389331031/ref=zg_bs_nav_automotive_2_5257480031",
            "https://www.amazon.in/gp/bestsellers/automotive/51419889031/ref=zg_bs_nav_automotive_2_5257480031",
            "https://www.amazon.in/gp/bestsellers/automotive/1389334031/ref=zg_bs_nav_automotive_2_5257480031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257591031/ref=zg_bs_nav_automotive_2_5257481031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258089031/ref=zg_bs_nav_automotive_3_5257591031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258090031/ref=zg_bs_nav_automotive_3_5258089031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258419031/ref=zg_bs_nav_automotive_4_5258090031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258420031/ref=zg_bs_nav_automotive_4_5258419031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258091031/ref=zg_bs_nav_automotive_3_5258089031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258421031/ref=zg_bs_nav_automotive_4_5258091031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348192031/ref=zg_bs_nav_automotive_2_5257482031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257600031/ref=zg_bs_nav_automotive_2_51348192031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348191031/ref=zg_bs_nav_automotive_2_5257600031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348195031/ref=zg_bs_nav_automotive_2_51348191031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257605031/ref=zg_bs_nav_automotive_2_51348195031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257606031/ref=zg_bs_nav_automotive_2_5257605031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257610031/ref=zg_bs_nav_automotive_2_5257606031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257598031/ref=zg_bs_nav_automotive_2_5257610031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257612031/ref=zg_bs_nav_automotive_2_5257598031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348193031/ref=zg_bs_nav_automotive_2_5257612031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348194031/ref=zg_bs_nav_automotive_2_51348193031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257613031/ref=zg_bs_nav_automotive_2_5257483031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348297031/ref=zg_bs_nav_automotive_3_5257613031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258144031/ref=zg_bs_nav_automotive_3_51348297031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257614031/ref=zg_bs_nav_automotive_2_5257483031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257619031/ref=zg_bs_nav_automotive_2_5257614031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257620031/ref=zg_bs_nav_automotive_2_5257614031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257621031/ref=zg_bs_nav_automotive_2_5257614031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257622031/ref=zg_bs_nav_automotive_2_5257614031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257623031/ref=zg_bs_nav_automotive_2_5257614031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258143031/ref=zg_bs_nav_automotive_3_5257623031",
            "https://www.amazon.in/gp/bestsellers/automotive/27316082031/ref=zg_bs_nav_automotive_3_5258143031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258144031/ref=zg_bs_nav_automotive_3_27316082031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258146031/ref=zg_bs_nav_automotive_3_5258144031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257622031/ref=zg_bs_nav_automotive_2_5257621031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258140031/ref=zg_bs_nav_automotive_3_5257622031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257512031/ref=zg_bs_nav_automotive_3_5257622031",
            "https://www.amazon.in/gp/bestsellers/automotive/5258429031/ref=zg_bs_nav_automotive_2_5257621031",
            "https://www.amazon.in/gp/bestsellers/automotive/7355649031/ref=zg_bs_nav_automotive_2_5257621031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257631031/ref=zg_bs_nav_automotive_2_5257484031",
            "https://www.amazon.in/gp/bestsellers/automotive/5257634031/ref=zg_bs_nav_automotive_2_5257631031",
            "https://www.amazon.in/gp/bestsellers/automotive/51348190031/ref=zg_bs_nav_automotive_2_5257634031",]
 

    while True:
        # loop through each URL and scrape data
        for base_url in urls:
            print("==========================#################===========================")
            print(base_url)
            print("==========================#################===========================")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

            # Define the CSV file and headers
            csv_file = 'Car Exterior Accessories.csv'
            csv_headers = ['Title', 'Description', 'Comment', 'Name', 'Video URL']

            product_links_csv_file = 'product_links_csv_file.csv'

            # Open the CSV file and write headers
            with open(csv_file, mode='w', newline='', encoding='utf-8', buffering=1) as file:
                writer = csv.writer(file)
                writer.writerow(csv_headers)

                # Loop through the pages
                for i in range(1, 9):
                    # Build the URL for the current page
                    url = f'{base_url}/ref=zg_bs_pg_2?ie=UTF8&pg={i}'
                    # Get the page content
                    page = requests.get(url, headers=headers)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    # Find all the products on the page
                    products = soup.find_all(id="gridItemRoot")

                    # Loop through the products
                    for product in products:
                        # Get the rank of the product
                        rank = product.find('span', class_="zg-bdg-text").text[1:]

                        # Get the product URL and ASIN
                        try:
                            link = product.find(
                                'a', class_='a-link-normal')['href']

                            product_url = f"https://www.amazon.in{link}"
                            # print (f"\n{product_url}\n")
                            asin = re.search(
                                r'/dp/([A-Z0-9]{10})/', product_url).group(1)
                        except:
                            pass
                        # Generate the affiliate URL
                        affiliate_id = "axiecart-21"
                        affiliate_url = f"https://www.amazon.in/dp/{asin}/?tag={affiliate_id}"

                        options = webdriver.ChromeOptions()
                        options.add_argument('--headless')

                        driver_path = '/path/to/chromedriver'
                        driver = webdriver.Chrome(
                            executable_path=driver_path, options=options)
                        driver.get(product_url)
                        html_content = driver.page_source

                        with open('amazon_product.html', 'w', encoding='utf-8') as f:
                            f.write(html_content)

                        driver.quit()

                        # Write the HTML content to a file

                        with open('amazon_product.html', 'r', encoding='utf-8') as f:
                            html = f.read()
                            soup = BeautifulSoup(html, 'html.parser')

                        video_urls = soup.find_all(
                            'div', {'id': 'ajaxBlockComponents_feature_div'})
                        ctr = 1

                        for video in video_urls:
                            try:
                                arr = video.find('script').text.split('"videos":"')
                                a = arr[0].index('{"dataInJson')
                                e = arr[0].index("}');")
                                new = arr[0][a:e+1]
                                new = json.loads(new)

                                for x in new['videos']:

                                    ctr += 1
                                    # print(f"\n\n{x['url']}\n\n")
                                    video_url = x['url']

                                    products_title = soup.find(
                                        id="productTitle").text.strip()

                                    yt_title_new = products_title.title()[:76]

                                    yt_replace = re.sub(
                                        r'[^\w\s]', '', yt_title_new)

                                    yt_title = f'latest Car Accessories: {yt_title_new}'

                                    products_description = soup.find(
                                        id="feature-bullets").text.replace('About this item ', '').strip()

                                    yt_description = f'latest Car Accessories: {products_title}\n\nBuy now on Amazon: Click the link- {affiliate_url} \n\n{products_description}'

                                    yt_comment = f'{yt_title_new}\n{affiliate_url}'
                                    youtube_video_titile.clear()
                                    youtube_video_description.clear()
                                    youtube_video_titile.append(yt_title_new)
                                    youtube_video_description.append(yt_description)

                                    with open('product_links_csv_file.csv', 'r') as file:
                                        reader = csv.reader(file)
                                        existing_product_urls = [
                                            row[0] for row in reader]
                                        print(existing_product_urls)
                                    product_urls = product_url
                                    if product_urls in existing_product_urls:
                                        print(
                                            " >>>>> product_urls already exists.<<<<<")

                                    else:
                                        existing_product_urls.append(product_urls)
                                        with open('product_links_csv_file.csv', 'w', newline='') as file:
                                            writer = csv.writer(file)
                                            for product_urls in existing_product_urls:
                                                writer.writerow([product_urls])
                                        print(
                                            ">>>>> product_urls added to the file. <<<<<")

                                        directorys = "C:/Users/New/AppData/Local/Programs/Python/Amazone"
                                        # List all files in the directory
                                        mp4files = os.listdir(directorys)
                                        count = 0

                                        for file in mp4files:
                                            if file.endswith('.mp4'):
                                                name = file
                                                os.remove(name)
                                        print("all vedio deleted")

                                        response = requests.get(video_url)

                                        with open("Product_Video.mp4", "wb") as f:
                                            f.write(response.content)
                                            video_cutt_logo()
                            except:
                                pass




video_scraping()
