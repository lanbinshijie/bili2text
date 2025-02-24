from src.config import *
import os
import subprocess
import glob
import src.log as log  # 使用 log 工具包

class Downloader:
    def __init__(self, video_dir="bilibili_video", output_dir="outputs"):
        self.video_dir = video_dir
        self.output_dir = output_dir
        self.ensure_folders_exist()

    def ensure_folders_exist(self):
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download_video(self, bv_number: str) -> str:
        if not bv_number.startswith("BV"):
            bv_number = "BV" + bv_number
        video_url = f"https://www.bilibili.com/video/{bv_number}"
        log.info(f"使用you-get下载视频: {video_url}")
        try:
            result = subprocess.run(
                ["you-get", "-o", self.video_dir, video_url],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                log.error(f"下载失败: {result.stderr}")
                return ""
            else:
                log.info(result.stdout)
                log.success(f"视频已成功下载到目录: {self.video_dir}")
                video_files = glob.glob(os.path.join(self.video_dir, "*.mp4"))
                if video_files:
                    latest_file = max(video_files, key=os.path.getmtime)
                    file_path = os.path.join(self.video_dir, f"{bv_number}.mp4")
                    os.rename(latest_file, file_path)
                    # 删除xml文件
                    xml_files = glob.glob(os.path.join(self.video_dir, "*.xml"))
                    for xml_file in xml_files:
                        os.remove(xml_file)
                    return file_path
                else:
                    log.warning("未找到下载的视频文件.")
                    return ""
        except Exception as e:
            log.error(f"发生错误: {str(e)}")
            return ""