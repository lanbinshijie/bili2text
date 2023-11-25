import whisper
import os
from tqdm import tqdm
whisper_model = whisper.load_model("small")

def run_analysis(filename, prompt="以下是普通话的句子。"):
    # 读取列表中的音频文件
    audio_list = os.listdir(f"audio/slice/{filename}")
    # 创建outputs文件夹
    os.makedirs("outputs", exist_ok=True)

    for fn in tqdm(audio_list, desc="Transcribing audio files", unit="file"):
        # 识别音频
        result = whisper_model.transcribe(f"audio/slice/{filename}/{fn}", initial_prompt=prompt)
        print("".join([i["text"] for i in result["segments"] if i is not None]))

        with open(f"outputs/{filename}.txt", "a", encoding="utf-8") as f:
            f.write("".join([i["text"] for i in result["segments"] if i is not None]))
            f.write("\n")
    

# run_analysis("20231125133459")