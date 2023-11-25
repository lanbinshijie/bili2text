import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser

def on_submit():
    # 获取视频链接
    video_link = video_link_entry.get()
    # TODO: 实现视频链接的处理逻辑
    print(f"视频链接: {video_link}")

def on_generate_again():
    # TODO: 实现再次生成的逻辑
    print("再次生成...")

def on_clear_log():
    # 清空日志框
    log_text.delete('1.0', END)

def on_show_result():
    # TODO: 显示结果到日志框的逻辑
    log_text.insert(END, "这里是结果...\n")

def on_select_model():
    selected_model = model_var.get()
    # TODO: 实现模型选择的逻辑
    print(f"选中的模型: {selected_model}")

def on_confirm_model():
    # 获取选中的模型
    selected_model = model_var.get()
    # TODO: 实现确认模型的逻辑
    print(f"确认的模型: {selected_model}")

# 创建窗口
app = ttk.Window("Bili2Text", themename="litera")
# 设置窗口大小820x540
app.geometry("820x540")

# 应用名
ttk.Label(app, text="Bili2Text", font=("Helvetica", 16)).pack(pady=10)

# 视频链接输入框和按钮
video_link_frame = ttk.Frame(app)
video_link_entry = ttk.Entry(video_link_frame)
video_link_entry.pack(side=LEFT, expand=YES, fill=X)
submit_button = ttk.Button(video_link_frame, text="提交", command=on_submit)
submit_button.pack(side=RIGHT)
video_link_frame.pack(fill=X, padx=20)

# 日志框
log_text = ttk.Text(app, height=10)
log_text.pack(padx=20, pady=10, fill=BOTH, expand=YES)

# 控件按钮的容器
controls_frame = ttk.Frame(app)
controls_frame.pack(fill=X, padx=20)

# 将按钮移动到控件容器中
generate_button = ttk.Button(controls_frame, text="再次生成", command=on_generate_again)
generate_button.pack(side=LEFT, padx=10, pady=10)

clear_log_button = ttk.Button(controls_frame, text="清空日志", command=on_clear_log, bootstyle=DANGER)
clear_log_button.pack(side=LEFT, padx=10, pady=10)

show_result_button = ttk.Button(controls_frame, text="展示结果", command=on_show_result)
show_result_button.pack(side=LEFT, padx=10, pady=10)

model_var = ttk.StringVar()
model_combobox = ttk.Combobox(controls_frame, textvariable=model_var, values=["tiny", "small", "medium", "large"])
model_combobox.pack(side=LEFT, padx=10, pady=10)
model_combobox.set("small") # 设置默认值

confirm_model_button = ttk.Button(controls_frame, text="确认模型", command=on_confirm_model)
confirm_model_button.pack(side=LEFT, padx=10, pady=10)

def open_github_link(event=None):
    webbrowser.open_new("https://github.com/lanbinshijie/bili2text")

# 页脚容器
footer_frame = ttk.Frame(app)
footer_frame.pack(side=BOTTOM, fill=X)

# 版本号 - 可以动态修改
version_label = ttk.Label(footer_frame, text="版本 1.0.0")
version_label.pack(side=LEFT, padx=10, pady=10)

# 固定的作者名称
author_label = ttk.Label(footer_frame, text="作者：Your Name")
author_label.pack(side=LEFT, padx=10, pady=10)

# GitHub链接 - 作为可点击的标签
# github_link = ttk.Label(footer_frame, text="开源仓库", foreground="blue", cursor="hand2")
# 设置为天蓝色
github_link = ttk.Label(footer_frame, text="开源仓库", cursor="hand2", bootstyle=PRIMARY)
github_link.pack(side=LEFT, padx=10, pady=10)
github_link.bind("<Button-1>", open_github_link)

app.mainloop()