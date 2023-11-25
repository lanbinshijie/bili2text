import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
import re
import sys, os
from downBili import download_video, bv2av
from exAudio import *
import threading
s2t = None

def open_popup(text, title="提示") -> ["cancelled", "confirmed"]:
    # 在屏幕中央显示弹窗
    # 创建一个弹窗
    popup = ttk.Toplevel()
    # popup = ttk.Window()
    popup.title("弹窗")
    popup.geometry("300x150")
    # 在屏幕中央显示弹窗
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) / 2
    y = (popup.winfo_screenheight() - popup.winfo_reqheight()) / 2
    popup.geometry("+%d+%d" % (x, y))
    

    # 添加标签
    label = ttk.Label(popup, text=text)
    label.pack(pady=10)

    # 使用一个变量来存储用户的选择
    user_choice = ttk.StringVar()

    # 确定按钮
    def on_confirm():
        user_choice.set("confirmed")
        popup.destroy()

    confirm_button = ttk.Button(popup, text="确定", style="primary.TButton", command=on_confirm)
    confirm_button.pack(side=LEFT, padx=10, pady=10)

    # 取消按钮
    def on_cancel():
        user_choice.set("cancelled")
        popup.destroy()

    cancel_button = ttk.Button(popup, text="取消", style="outline-danger.TButton", command=on_cancel)
    cancel_button.pack(side=RIGHT, padx=10, pady=10)

    # 等待弹窗关闭
    popup.wait_window()

    # 返回用户的选择
    return user_choice.get()

def showlog(text, state="INFO"):
    # 先设置为可编辑
    log_text.config(state="normal")
    # 插入日志
    log_text.insert(END, f"[LOG][{state}] " + text + "\n")
    # 设置为不可编辑
    log_text.config(state="disabled")

def on_submit():
    if s2t == None:
        print("Whisper未加载！")
        return
    # 获取视频链接
    video_link = video_link_entry.get()
    if video_link == "":
        print("视频链接不能为空！")
        return
    if open_popup("是否确定生成？可能耗费时间较长", title="提示") == "cancelled":
        return

    # TODO: 实现视频链接的处理逻辑
    pattern = r'BV[A-Za-z0-9]+' # 正则表达式
    match = re.findall(pattern, video_link)
    match = match[0]

    print(f"视频链接: {video_link}")
    print(f"BV号: {match}")
    av = bv2av(match)
    print(f"AV号: {av}")
    thread = threading.Thread(target=process_video, args=(av,))
    thread.start()


def process_video(av):
    print("="*10)
    print("正在下载视频...")
    filename = download_video(str(av))
    print("="*10)
    print("正在分割音频...")
    foldername = run_split(filename)
    print("="*10)
    print("正在转换文本（可能耗时较长）...")
    s2t.run_analysis(foldername, prompt="以下是普通话的句子。这是一个关于{}的视频。".format(filename))
    output_path = f"outputs/{foldername}.txt"
    print("转换完成！", output_path)


def on_generate_again():
    # TODO: 实现再次生成的逻辑
    print("再次生成...")
    print(open_popup("是否再次生成？"))

def on_clear_log():
    # 清空日志框
    log_text.delete('1.0', END)

def on_show_result():
    # TODO: 显示结果到日志框的逻辑
    # log_text.insert(END, "这里是结果...\n")
    # print("这里是结果...")
    print("这里是结果...")

def on_select_model():
    selected_model = model_var.get()
    # TODO: 实现模型选择的逻辑
    print(f"选中的模型: {selected_model}")

def on_confirm_model():
    # 获取选中的模型
    selected_model = model_var.get()
    # TODO: 实现确认模型的逻辑
    print(f"确认的模型: {selected_model}")

def load_whisper():
    global s2t
    import speech2text
    s2t = speech2text
    s2t.load_whisper(model=model_var.get())
    print("加载Whisper成功！")


# 创建窗口
app = ttk.Window("Bili2Text - By Lanbin | www.lanbin.top", themename="litera")
# 设置窗口大小820x540
app.geometry("820x540")

# 应用名
ttk.Label(app, text="Bilibili To Text", font=("Helvetica", 16)).pack(pady=10)

# 视频链接输入框和按钮
video_link_frame = ttk.Frame(app)
video_link_entry = ttk.Entry(video_link_frame)
video_link_entry.pack(side=LEFT, expand=YES, fill=X)
loadWhisper = ttk.Button(video_link_frame, text="加载Whisper", command=load_whisper, bootstyle="success-outline")
loadWhisper.pack(side=RIGHT, padx=5)
submit_button = ttk.Button(video_link_frame, text="下载视频", command=on_submit)
submit_button.pack(side=RIGHT, padx=5)
video_link_frame.pack(fill=X, padx=20)

# 日志框
log_text = ttk.ScrolledText(app, height=10, state="disabled")
log_text.pack(padx=20, pady=10, fill=BOTH, expand=YES)

# 控件按钮的容器
controls_frame = ttk.Frame(app)
controls_frame.pack(fill=X, padx=20)

# 将按钮移动到控件容器中
generate_button = ttk.Button(controls_frame, text="再次生成", command=on_generate_again)
generate_button.pack(side=LEFT, padx=10, pady=10)

show_result_button = ttk.Button(controls_frame, text="展示结果", command=on_show_result, bootstyle="success-outline")
show_result_button.pack(side=LEFT, padx=10, pady=10)

model_var = ttk.StringVar(value="medium")
model_combobox = ttk.Combobox(controls_frame, textvariable=model_var, values=["tiny", "small", "medium", "large"])
model_combobox.pack(side=LEFT, padx=10, pady=10)
model_combobox.set("small") # 设置默认值

confirm_model_button = ttk.Button(controls_frame, text="确认模型", command=on_confirm_model, bootstyle="primary-outline")
confirm_model_button.pack(side=LEFT, padx=10, pady=10)

clear_log_button = ttk.Button(controls_frame, text="清空日志", command=on_clear_log, bootstyle=DANGER)
clear_log_button.pack(side=LEFT, padx=10, pady=10)

def open_github_link(event=None):
    webbrowser.open_new("https://github.com/lanbinshijie/bili2text")

# 页脚容器
footer_frame = ttk.Frame(app)
footer_frame.pack(side=BOTTOM, fill=X)

# 固定的作者名称
author_label = ttk.Label(footer_frame, text="作者：Lanbin")
author_label.pack(side=LEFT, padx=10, pady=10)

# 版本号 - 可以动态修改
versionVar = ttk.StringVar(value="1.0.0")
version_label = ttk.Label(footer_frame, text="版本 " + versionVar.get(), foreground="gray")
version_label.pack(side=LEFT, padx=10, pady=10)

# GitHub链接 - 作为可点击的标签
github_link = ttk.Label(footer_frame, text="开源仓库", cursor="hand2", bootstyle=PRIMARY)
github_link.pack(side=LEFT, padx=10, pady=10)
github_link.bind("<Button-1>", open_github_link)

def fn_SYSTEM_IO_REDIRECT():
    # 重定向标准输出和标准错误到日志框
    class StdoutRedirector(object):
        def write(self, message, state="INFO"):
            # log_text.insert(END, f"[LOG][{state}] " + message + "\n")
            if message != "\n" and message != "\r" and "Speed" not in message:
                log_text.config(state=NORMAL)
                log_text.insert(END, f"[LOG][{state}] {message}\n")
                log_text.config(state=DISABLED)
                log_text.see(END)
        def flush(self):
            pass
    sys.stdout = StdoutRedirector()
    sys.stderr = StdoutRedirector()

# 调用此函数以开始重定向输出
fn_SYSTEM_IO_REDIRECT()


app.mainloop()
