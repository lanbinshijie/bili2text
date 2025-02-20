from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import time

def convert_flv_to_mp3(name, target_name=None, folder='bilibili_video'):
    # 提取视频中的音频并保存为 MP3 到 audio/conv 目录
    clip = VideoFileClip(f'{folder}/{name}.mp4')
    audio = clip.audio
    os.makedirs("audio/conv", exist_ok=True)
    output_name = target_name if target_name else name
    audio.write_audiofile(f"audio/conv/{output_name}.mp3")

def split_mp3(filename, folder_name, slice_length=45000, target_folder="audio/slice"):
    audio = AudioSegment.from_mp3(filename)
    total_slices = len(audio) // slice_length
    target_dir = os.path.join(target_folder, folder_name)
    os.makedirs(target_dir, exist_ok=True)
    for i in range(total_slices):
        start = i * slice_length
        end = start + slice_length
        slice_audio = audio[start:end]
        slice_path = os.path.join(target_dir, f"{i+1}.mp3")
        slice_audio.export(slice_path, format="mp3")
        print(f"Slice {i+1} saved: {slice_path}")

def process_audio_split(name):
    # 生成唯一文件夹名，并依次调用转换和分割函数
    folder_name = time.strftime('%Y%m%d%H%M%S')
    convert_flv_to_mp3(name, target_name=folder_name)
    conv_file = f"audio/conv/{folder_name}.mp3"
    split_mp3(conv_file, folder_name)
    return folder_name

