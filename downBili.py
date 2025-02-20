import requests
import time
import os
import sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/55.0.2883.87 Safari/537.36'
}

def ensure_folders_exist():
    for folder in ["bilibili_video", "outputs"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def download_video(bv_number):
    try:
        meta_url = f"https://bili.zhouql.vip/meta/{bv_number}"
        meta_response = requests.get(meta_url)
        meta_data = meta_response.json()
        if meta_data.get("code") != 0:
            print("元数据请求失败:", meta_data.get("message"))
            return
        cid = meta_data["data"]["cid"]
        aid = meta_data["data"]["aid"]
        print(f"获取的cid: {cid}, aid: {aid}")

        download_url = f"https://bili.zhouql.vip/download/{aid}/{cid}"
        download_response = requests.get(download_url)
        download_data = download_response.json()
        if download_data.get("code") != 0:
            print("下载链接请求失败:", download_data.get("message"))
            return
        video_url = download_data["data"]["durl"][0]["url"]
        print(f"视频下载链接: {video_url}")

        ensure_folders_exist()
        file_path = f"bilibili_video/{bv_number}.mp4"
        video_response = requests.get(video_url, stream=True, headers=HEADERS)
        total_size = int(video_response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(file_path, "wb") as wf:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    wf.write(chunk)
                    downloaded_size += len(chunk)
                    percent_complete = downloaded_size / total_size * 100
                    progress = int(percent_complete // 2)
                    sys.stdout.write(f"\r下载进度: [{'#' * progress}{' ' * (50 - progress)}] {percent_complete:.2f}%")
                    sys.stdout.flush()
        print(f"\n视频已成功下载到: {file_path}")
        return bv_number
    except Exception as e:
        print("发生错误:", str(e))