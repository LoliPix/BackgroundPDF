import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from PIL import Image, ImageTk
import sys

def select_files():
    """打开文件选择对话框，允许选择多个PDF文件"""
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        # 将多个文件路径以列表形式存储
        entry_input.set(";".join(file_paths))

def select_output_folder():
    """打开输出文件夹选择对话框"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output.set(folder_path)

def choose_color():
    """打开颜色选择对话框"""
    color = colorchooser.askcolor(title="选择背景颜色")[1]
    if color:
        entry_color.set(color)

def process_pdf():
    """批量处理PDF文件"""
    input_pdfs = entry_input.get().split(";")
    output_folder = entry_output.get()
    bg_color = entry_color.get()

    if not input_pdfs or not output_folder or not bg_color:
        messagebox.showwarning("警告", "请填写所有必要信息。")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 将十六进制颜色转换为RGB
    r = int(bg_color[1:3], 16) / 255.0
    g = int(bg_color[3:5], 16) / 255.0
    b = int(bg_color[5:7], 16) / 255.0
    
    total_files = len(input_pdfs)
    for i, input_pdf in enumerate(input_pdfs):
        if not os.path.exists(input_pdf):
            messagebox.showerror("错误", f"文件不存在：{input_pdf}")
            continue

        try:
            # 打开输入PDF
            doc = fitz.open(input_pdf)
            
            # 创建一个自定义颜色的背景PDF
            background_pdf = fitz.open()
            for page in doc:
                new_page = background_pdf.new_page(width=page.rect.width, height=page.rect.height)
                # 设置自定义背景颜色
                new_page.draw_rect(new_page.rect, color=(r, g, b), fill=(r, g, b))
                # 将原PDF页面内容合并到背景上
                new_page.show_pdf_page(new_page.rect, doc, page.number, keep_proportion=True, rotate=0)
            
            # 保存到输出PDF
            output_pdf = os.path.join(output_folder, f"bg_{os.path.basename(input_pdf)}")
            background_pdf.save(output_pdf)
            background_pdf.close()
            doc.close()
            # 更新进度
            progress_var.set(f"已处理 {i+1}/{total_files} 个文件")
        except Exception as e:
            messagebox.showerror("错误", f"处理 {os.path.basename(input_pdf)} 时发生错误：{str(e)}")

    messagebox.showinfo("完成", f"所有文件已处理，输出文件夹：{output_folder}")

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.geometry("400x600")

    # 您的个人信息
    ttk.Label(about_window, text="关于", font=("Arial", 16, "bold")).pack(pady=10)
    
    # 使用超链接标签
    github_link = ttk.Label(about_window, text="GitHub: github.com/LoliPix", foreground="blue", cursor="hand2")
    github_link.pack()
    github_link.bind("<Button-1>", lambda e: callback("https://github.com/LoliPix"))
    
    bilibili_link = ttk.Label(about_window, text="B站: space.bilibili.com/638406047", foreground="blue", cursor="hand2")
    bilibili_link.pack()
    bilibili_link.bind("<Button-1>", lambda e: callback("https://space.bilibili.com/638406047"))

    # 支付二维码
    try:
        # 确定图片路径
        if getattr(sys, 'frozen', False):
            # 打包后使用资源路径
            qr_image_path = os.path.join(sys._MEIPASS, "pay.jpg")
        else:
            # 开发环境中使用相对路径
            qr_image_path = "pay.jpg"
        qr_image = Image.open(qr_image_path)
        
        # 计算缩放比例，保持图片长宽比
        original_width, original_height = qr_image.size
        scale = min(300 / original_width, 300 / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        qr_image = qr_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(qr_image)
        qr_label = ttk.Label(about_window, image=photo)
        qr_label.image = photo  # 保持引用
        qr_label.pack(pady=20)
    except FileNotFoundError:
        ttk.Label(about_window, text="支付二维码图片文件未找到，请检查路径是否正确。").pack()
    except PermissionError:
        ttk.Label(about_window, text="无法访问支付二维码图片，可能是权限问题。").pack()
    except ValueError:
        ttk.Label(about_window, text="图片格式可能不受支持，请确保是JPG或PNG格式。").pack()
    except Exception as e:
        ttk.Label(about_window, text=f"无法加载支付二维码：{str(e)}").pack()

    # 添加一些关于捐赠的说明文字
    ttk.Label(about_window, text="如果您喜欢这个工具，欢迎支持开发者。\n捐赠是自愿的，但您的支持将帮助我们持续开发。", justify=tk.CENTER).pack(pady=10)

    # 添加一个按钮或链接来关闭窗口或返回
    ttk.Button(about_window, text="关闭", command=about_window.destroy).pack(pady=10)

def callback(url):
    import webbrowser
    webbrowser.open_new(url)

# 创建主窗口
root = tk.Tk()
root.title("PDF背景颜色批量修改器")
root.geometry("500x250")

# 应用样式
style = ttk.Style()
style.theme_use('clam')  # 使用更现代的样式

# 使用变量来存储用户输入
entry_input = tk.StringVar()
entry_output = tk.StringVar()
entry_color = tk.StringVar()
progress_var = tk.StringVar()

# 布局框架
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# 输入PDF路径
ttk.Label(mainframe, text="选择PDF文件:").grid(column=1, row=1, sticky=tk.W)
ttk.Entry(mainframe, width=40, textvariable=entry_input).grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
ttk.Button(mainframe, text="浏览", command=select_files).grid(column=4, row=1)

# 选择输出文件夹
ttk.Label(mainframe, text="输出文件夹:").grid(column=1, row=2, sticky=tk.W)
ttk.Entry(mainframe, width=40, textvariable=entry_output).grid(column=2, row=2, columnspan=2, sticky=(tk.W, tk.E))
ttk.Button(mainframe, text="浏览", command=select_output_folder).grid(column=4, row=2)

# 选择背景颜色
ttk.Label(mainframe, text="背景颜色:").grid(column=1, row=3, sticky=tk.W)
ttk.Entry(mainframe, width=10, textvariable=entry_color).grid(column=2, row=3, sticky=tk.W)
ttk.Button(mainframe, text="选择颜色", command=choose_color).grid(column=3, row=3, sticky=tk.W)

# 处理PDF按钮
ttk.Button(mainframe, text="批量处理PDF", command=process_pdf).grid(column=2, row=4, sticky=tk.W, pady=10)

# 关于按钮
ttk.Button(mainframe, text="关于", command=open_about).grid(column=4, row=4, sticky=tk.E, pady=10)

# 显示处理进度
ttk.Label(mainframe, textvariable=progress_var).grid(column=2, row=5, columnspan=2, sticky=(tk.W, tk.E))

# 调整间距
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# 设置窗口图标（如果有）
try:
    root.iconbitmap(default=r"E:\Documents\iconfont.ico")
except Exception:
    pass  # 忽略设置图标的错误

# 运行主循环
root.mainloop()
