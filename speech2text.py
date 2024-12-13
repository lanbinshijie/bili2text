import platform
import whisper
import os
import torch

whisper_model = None

def get_available_device():
    if torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'

def load_whisper(model="tiny"):
    global whisper_model
    device = get_available_device()
    whisper_model = whisper.load_model(model, device=device)
    print(f"Whisper模型：{model}")
    print(f"使用了{device.upper()}计算单元提取，您的电脑{'可用显卡加速' if device != 'cpu' else '不支持显卡加速'}")

def run_analysis(filename, model="tiny", prompt="以下是普通话的句子。"):
    global whisper_model
    print("正在加载Whisper模型...")
    # 读取列表中的音频文件
    audio_list = os.listdir(f"audio/slice/{filename}")
    print("加载Whisper模型成功！")
    # 创建outputs文件夹
    os.makedirs("outputs", exist_ok=True)
    print("正在转换文本...")

    i = 1
    for fn in audio_list:
        print(f"正在转换第{i}/{len(audio_list)}个音频... {fn}")
        # 识别音频
        result = whisper_model.transcribe(f"audio/slice/{filename}/{fn}", initial_prompt=prompt)
        print("".join([i["text"] for i in result["segments"] if i is not None]))

        with open(f"outputs/{filename}.txt", "a", encoding="utf-8") as f:
            f.write("".join([i["text"] for i in result["segments"] if i is not None]))
            f.write("\n")
        i += 1
