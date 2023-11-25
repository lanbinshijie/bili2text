from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import time

def flv_mp3(name, target_name=None, folder='bilibili_video'):
    # 将FLV视频文件加载为一个VideoFileClip对象
    clip = VideoFileClip(f'{folder}/{name}/{name}.flv')
    # 提取音频部分
    audio = clip.audio
    # 创建audio/conv文件夹（如果不存在
    os.makedirs("audio/conv", exist_ok=True)
    # 将音频保存为一个文件（例如MP3），写入conv文件夹
    audio.write_audiofile(f"audio/conv/{name if not target_name else target_name}.mp3")



def split_mp3(filename, folder_name, slice_length=60000, target_folder="audio/slice"):
    # 加载MP3文件
    audio = AudioSegment.from_mp3(filename)

    # 计算分割的数量
    total_slices = len(audio) // slice_length

    # 确保目标文件夹存在
    os.makedirs(os.path.join(target_folder, folder_name), exist_ok=True)

    for i in range(total_slices):
        # 分割音频
        start = i * slice_length
        end = start + slice_length
        slice = audio[start:end]

        # 构建保存路径
        slice_filename = f"{folder_name}/{i+1}.mp3"
        slice_path = os.path.join(target_folder, slice_filename)

        # 导出分割的音频片段
        slice.export(slice_path, format="mp3")
        print(f"Slice {i} saved: {slice_path}")

# 使用示例
def run_split(name):
    folder_name = f"{time.strftime('%Y%m%d%H%M%S')}"
    flv_mp3(name, target_name=folder_name)
    split_mp3(f"audio/conv/{folder_name}.mp3", folder_name)
    return folder_name

if __name__ == '__main__':
    print(run_split("梦想中的截图工具，终于有人做出来了！"))
