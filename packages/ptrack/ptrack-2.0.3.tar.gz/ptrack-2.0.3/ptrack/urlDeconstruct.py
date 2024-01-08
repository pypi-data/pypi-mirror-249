import requests
from bs4 import BeautifulSoup
import subprocess
from tempfile import NamedTemporaryFile
from yt_dlp import main as yt_dlp
import json
import ascii_magic
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from urllib3 import PoolManager


def getData(url):
    process = subprocess.Popen(['yt-dlp', '--format',  'bestvideo+bestaudio/best', url, '--dump-json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        print(f"Error: {err}")
        return None
    try:
        data = json.loads(out)
        return data
    except json.JSONDecodeError:
        print("Failed to decode JSON from yt-dlp output.")



def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        with NamedTemporaryFile(delete=False, suffix='.png') as img_temp:
            img = Image.open(requests.get(url, stream=True).raw)
            img.save(img_temp, 'PNG')
            return img_temp.name
    return None

def send_notification(title, message, image_url):
    local_image_path = download_image(image_url)
    if local_image_path:
        subprocess.run(['notify-send', title, message, '-i', local_image_path])
        subprocess.run(['rm', local_image_path])
    else:
        subprocess.run(['notify-send', title, message])

def getFileSize(url):
    http = PoolManager()
    r = http.request('HEAD', url)
    size = int(r.headers['Content-Length'])
    return size if size else 0

def find_media_urls(url):
    try:
        ydl_data = getData(url)
        if not ydl_data:
            return []

        title = ydl_data['title']
        video_url = ydl_data['requested_formats'][0]['url']
        audio_url = ydl_data['requested_formats'][1]['url']

        video_size, accuracy = (ydl_data['requested_formats'][0]['filesize'], True) if 'filesize' in ydl_data['requested_formats'][0] else (ydl_data['requested_formats'][0]['filesize_approx'], True) if 'filesize_approx' in ydl_data['requested_formats'][0] else (getFileSize(video_url), False)
        audio_size, accuracy = (ydl_data['requested_formats'][1]['filesize'], accuracy) if 'filesize' in ydl_data['requested_formats'][1] else (ydl_data['requested_formats'][1]['filesize_approx'], accuracy) if 'filesize_approx' in ydl_data['requested_formats'][1] else (getFileSize(audio_url), False)

        size = video_size + audio_size
        thumbnail_url = next((item['url'] for item in ydl_data['thumbnails'] if 'height' in item and item['height'] == 360), None)

        if thumbnail_url:
            send_notification("Download Started", title, thumbnail_url)

        return [(video_url, audio_url, title, size, accuracy)]

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return []



def get_urls(urls):
    RESULTS = []

    for url in urls:
        media_urls = find_media_urls(url)
        RESULTS.extend(media_urls)

    return RESULTS
