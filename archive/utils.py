import os
import subprocess
import glob  # 新增导入

def ensure_folders_exist():
    if not os.path.exists("bilibili_video"):
        os.makedirs("bilibili_video")
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

def download_video(bv_number):
    """
    使用you-get下载B站视频。
    参数:
        bv_number: 字符串形式的BV号（不含"BV"前缀）或完整BV号
    返回:
        文件路径
    """
    if not bv_number.startswith("BV"):
        bv_number = "BV" + bv_number
    video_url = f"https://www.bilibili.com/video/{bv_number}"
    ensure_folders_exist()
    output_dir = "bilibili_video"
    print(f"使用you-get下载视频: {video_url}")
    try:
        result = subprocess.run(["you-get", "-o", output_dir, video_url], capture_output=True, text=True)
        if result.returncode != 0:
            print("下载失败:", result.stderr)
        else:
            print(result.stdout)
            print(f"视频已成功下载到目录: {output_dir}")
            # 重命名下载的视频文件，假设下载的为最新的 .mp4 文件
            video_files = glob.glob(os.path.join(output_dir, "*.mp4"))
            if video_files:
                latest_file = max(video_files, key=os.path.getmtime)
                file_path = f"{output_dir}/{bv_number}.mp4"
                os.rename(latest_file, file_path)
                # 删除xml文件
                xml_files = glob.glob(os.path.join(output_dir, "*.xml"))
                for xml_file in xml_files:
                    os.remove(xml_file)
            else:
                file_path = ""
    except Exception as e:
        print("发生错误:", str(e))
        file_path = ""
    return bv_number
