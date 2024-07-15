from downBili import download_video
from exAudio import *
from speech2text import *
# from xunfei import *

# md5加密取前8位作为文件夹名

# load_whisper("small")
# filename = "张骞出使西域各国"
# # foldername = run_split("16ad48bc")

# run_analysis("20231128195013", prompt="以下是普通话的句子。")
# output_path = f"outputs/2440bfdb.txt"
# exit()

av = input("请输入av号：")
filename = download_video(av)
foldername = run_split(filename)

# audio_list = os.listdir(f"audio/slice/{foldername}")
# i = 1
# for fn in audio_list:
#     print(f"正在转换第{i}/{len(audio_list)}个音频... {fn}")
#     # 识别音频
#     result = doRequest(foldername, fn)
#     print("".join([i["text"] for i in result["segments"] if i is not None]))

#     with open(f"outputs/{filename}.txt", "a", encoding="utf-8") as f:
#         f.write("".join([i["text"] for i in result["segments"] if i is not None]))
#         f.write("\n")
#     i += 1

load_whisper("small")
run_analysis(foldername, prompt="以下是普通话的句子。")
output_path = f"outputs/{foldername}.txt"
print("转换完成！", output_path)
