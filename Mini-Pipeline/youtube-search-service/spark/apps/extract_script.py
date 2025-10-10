import os
import re
import time
import uuid

from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
import yt_dlp
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}

def get_youtube_video_info(video_url):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        return {
            "video_id": video_info['id'],
            "title": video_info['title'],
            "upload_date": video_info['upload_date'],
            "channel": video_info['channel'],
            "duration": video_info['duration_string']
        }

def get_video_id(video_url):
    return video_url.split('v=')[1][:11]

def preprocessing(text):
    text = re.sub(r'(\(.+?\))', '', text)
    text = re.sub(r'(\[.+?\])', '', text)
    text = re.sub(r'[\\/:*?"<>|.]', '_', text)
    text = re.sub(r"[^\sa-zA-Z0-9ㄱ-ㅎ가-힣!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)※‘’·“”㈜ⓒ™©•]", '', text).strip()
    return text

def extract_script(channel_code, max_video=100000):
    download_folder = os.path.join('download_folder', channel_code)
    os.makedirs(download_folder, exist_ok=True)

    driver = webdriver.Chrome()
    playlist_url = f"https://www.youtube.com/playlist?list={channel_code}"
    driver.get(playlist_url)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(10)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    url_list = ['https://www.youtube.com' + s['href'] for s in soup.find_all(id='video-title') if s.get('href')]

    print(">> VIDEO LIST SCANNED:", len(url_list))
    count = 0

    for video_url in tqdm(url_list):
        video_id = get_video_id(video_url)
        try:
            info = get_youtube_video_info(video_url)
            title = preprocessing(info["title"])
            date = info["upload_date"]
        except Exception as e:
            print(f"[ERROR] yt_dlp: {e}")
            continue

        try:
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=['ko'])
        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"[INFO] No transcript for {video_id}")
            continue
        except Exception as e:
            print(f"[ERROR] TranscriptAPI: {e}")
            continue

        text_formatted = " ".join([item.text for item in transcript])

        row = "\n".join([
            str(uuid.uuid4()),
            video_id,
            title,
            date,
            text_formatted,
            'ko',
            "", "", "", "", ""
        ])

        file_path = os.path.join(download_folder, f"{title}.txt")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(row)
        except Exception as e:
            print(f"[ERROR] File write: {e}")

        count += 1
        if count >= max_video:
            break

if __name__ == "__main__":
    channel_code = "PL9a4x_yPK_86-3n5ggM7jescX0Q4770iU"
    extract_script(channel_code, 10)
