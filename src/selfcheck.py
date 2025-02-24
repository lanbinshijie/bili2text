import os
import subprocess
import src.log as log

# output/
#  - tmp：储存下载的视频/转换的音频等临时文件
#    - videos：储存下载的视频
#    - audios：储存转换的音频
#  - result：输出的稿件位置
#  - meta：储存一个转换的元数据（标题、地址、时长、作者、BV号，视频文件地址、文字稿件地址）

def ensure_folders_exist():
    try:
        if not os.path.exists("output"):
            os.makedirs("output")
        if not os.path.exists("output/tmp"):
            os.makedirs("output/tmp")
        if not os.path.exists("output/tmp/videos"):
            os.makedirs("output/tmp/videos")
        if not os.path.exists("output/tmp/audios"):
            os.makedirs("output/tmp/audios")
        if not os.path.exists("output/result"):
            os.makedirs("output/result")
        if not os.path.exists("output/meta"):
            os.makedirs("output/meta")
    except Exception as e:
        log.error(f"创建文件夹失败：{str(e)}，请检查权限并重试。")
        return False

# 检测是否有ffmpeg
def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            log.error("检测到没有安装ffmpeg，请安装后再试。")
            return False
        else:
            return True
    except FileNotFoundError:
        log.error("检测到没有安装ffmpeg，请安装后再试。")
        return False
    
def check_you_get():
    try:
        result = subprocess.run(["you-get", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            log.error("检测到没有安装you-get，请安装后再试。")
            return False
        else:
            return True
    except FileNotFoundError:
        log.error("检测到没有安装you-get，请安装后再试。")
        return False
    
class SelfCheck:
    def __init__(self):
        self.checks = [
            check_ffmpeg,
            check_you_get
        ]
        
    def run(self):
        log.info("开始自检...")
        ensure_folders_exist()
        for check in self.checks:
            if not check():
                log.error("自检失败，请检查错误信息并修复后再试。")
                return False
        log.success("自检通过！")
        return True