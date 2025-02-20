import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
import re
import sys
import threading
from utils import download_video
from exAudio import convert_flv_to_mp3, split_mp3, process_audio_split

speech_to_text = None  # 模型实例

def is_cuda_available(whisper):
    return whisper.torch.cuda.is_available()

def open_popup(text, title="提示"):

    popup = ttk.Toplevel()
    popup.title(title)
    popup.geometry("300x150")
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) // 2
    y = (popup.winfo_screenheight() - popup.winfo_reqheight()) // 2
    popup.geometry("+%d+%d" % (x, y))
    label = ttk.Label(popup, text=text)
    label.pack(pady=10)
    user_choice = ttk.StringVar()

    def on_confirm():
        user_choice.set("confirmed")
        popup.destroy()
    confirm_button = ttk.Button(popup, text="确定", style="primary.TButton", command=on_confirm)
    confirm_button.pack(side=LEFT, padx=10, pady=10)

    def on_cancel():
        user_choice.set("cancelled")
        popup.destroy()
    cancel_button = ttk.Button(popup, text="取消", style="outline-danger.TButton", command=on_cancel)
    cancel_button.pack(side=RIGHT, padx=10, pady=10)
    popup.wait_window()
    return user_choice.get()

def show_log(text, state="INFO"):

    log_text.config(state="normal")
    log_text.insert(END, f"[LOG][{state}] {text}\n")
    log_text.config(state="disabled")

def on_submit_click():
    global speech_to_text
    if speech_to_text is None:
        print("Whisper未加载！请点击加载Whisper按钮。")
        return
    video_link = video_link_entry.get()
    if not video_link:
        print("视频链接不能为空！")
        return
    if open_popup("是否确定生成？可能耗费时间较长", title="提示") == "cancelled":
        return
    # 提取BV号
    pattern = r'BV[A-Za-z0-9]+'
    matches = re.findall(pattern, video_link)
    if not matches:
        print("无效的视频链接！")
        return
    bv_number = matches[0]
    print(f"视频链接: {video_link}, BV号: {bv_number}")
    thread = threading.Thread(target=process_video, args=(bv_number[2:],))
    thread.start()

def process_video(av_number):
    print("=" * 10)
    print("正在下载视频...")
    file_identifier = download_video(str(av_number))
    print("=" * 10)
    print("正在分割音频...")
    # 使用音频模块处理
    folder_name = process_audio_split(file_identifier)
    print("=" * 10)
    print("正在转换文本（可能耗时较长）...")
    speech_to_text.run_analysis(folder_name, 
        prompt="以下是普通话的句子。这是一个关于{}的视频。".format(file_identifier))
    output_path = f"outputs/{folder_name}.txt"
    print("转换完成！", output_path)

def on_generate_again_click():
    print("再次生成...")
    print(open_popup("是否再次生成？"))

def on_clear_log_click():
    log_text.delete('1.0', END)

def on_show_result_click():
    print("这里是结果...")

def on_select_model():
    selected_model = model_var.get()
    print(f"选中的模型: {selected_model}")
    print("请点击加载Whisper按钮加载模型！")

def on_confirm_model_click():
    selected_model = model_var.get()
    print(f"确认的模型: {selected_model}")
    print("请点击加载Whisper按钮加载模型！")

def load_whisper_model():
    global speech_to_text
    import speech2text
    speech_to_text = speech2text
    speech_to_text.load_whisper(model=model_var.get())
    msg = "CUDA加速已启用" if is_cuda_available(speech_to_text.whisper) else "使用CPU计算"
    print("加载Whisper成功！", msg)

def open_github_link(event=None):
    webbrowser.open_new("https://github.com/lanbinshijie/bili2text")

def redirect_system_io():
    class StdoutRedirector:
        def write(self, message, state="INFO"):
            if message.strip() and "Speed" not in message:
                log_text.config(state=NORMAL)
                log_text.insert(END, f"[LOG][{state}] {message}\n")
                log_text.config(state=DISABLED)
                log_text.see(END)
        def flush(self):
            pass
    sys.stdout = StdoutRedirector()
    sys.stderr = StdoutRedirector()

def main():
    global video_link_entry, log_text, model_var
    app = ttk.Window("Bili2Text - By Lanbin | www.lanbin.top", themename="litera")
    app.geometry("820x540")
    app.iconbitmap("favicon.ico")
    ttk.Label(app, text="Bilibili To Text", font=("Helvetica", 16)).pack(pady=10)
    
    video_link_frame = ttk.Frame(app)
    video_link_entry = ttk.Entry(video_link_frame)
    video_link_entry.pack(side=LEFT, expand=YES, fill=X)
    load_whisper_button = ttk.Button(video_link_frame, text="加载Whisper", command=load_whisper_model, bootstyle="success-outline")
    load_whisper_button.pack(side=RIGHT, padx=5)
    submit_button = ttk.Button(video_link_frame, text="下载视频", command=on_submit_click)
    submit_button.pack(side=RIGHT, padx=5)
    video_link_frame.pack(fill=X, padx=20)
    
    log_text = ttk.ScrolledText(app, height=10, state="disabled")
    log_text.pack(padx=20, pady=10, fill=BOTH, expand=YES)
    
    controls_frame = ttk.Frame(app)
    controls_frame.pack(fill=X, padx=20)
    generate_button = ttk.Button(controls_frame, text="再次生成", command=on_generate_again_click)
    generate_button.pack(side=LEFT, padx=10, pady=10)
    show_result_button = ttk.Button(controls_frame, text="展示结果", command=on_show_result_click, bootstyle="success-outline")
    show_result_button.pack(side=LEFT, padx=10, pady=10)
    
    model_var = ttk.StringVar(value="medium")
    model_combobox = ttk.Combobox(controls_frame, textvariable=model_var, values=["tiny", "small", "medium", "large"])
    model_combobox.pack(side=LEFT, padx=10, pady=10)
    model_combobox.set("small")
    
    confirm_model_button = ttk.Button(controls_frame, text="确认模型", command=on_confirm_model_click, bootstyle="primary-outline")
    confirm_model_button.pack(side=LEFT, padx=10, pady=10)
    
    clear_log_button = ttk.Button(controls_frame, text="清空日志", command=on_clear_log_click, bootstyle=DANGER)
    clear_log_button.pack(side=LEFT, padx=10, pady=10)
    
    footer_frame = ttk.Frame(app)
    footer_frame.pack(side=BOTTOM, fill=X)
    author_label = ttk.Label(footer_frame, text="作者：Lanbin")
    author_label.pack(side=LEFT, padx=10, pady=10)
    version_var = ttk.StringVar(value="2.0.0")
    version_label = ttk.Label(footer_frame, text="版本 " + version_var.get(), foreground="gray")
    version_label.pack(side=LEFT, padx=10, pady=10)
    github_link = ttk.Label(footer_frame, text="开源仓库", cursor="hand2", bootstyle=PRIMARY)
    github_link.pack(side=LEFT, padx=10, pady=10)
    github_link.bind("<Button-1>", open_github_link)
    
    redirect_system_io()
    app.mainloop()

if __name__ == "__main__":
    main()
