import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


current_image = None  # 保存当前生成的原图


def generate_image(event=None):
    global current_image
    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        block = int(entry_block.get())

        fg = (
            int(entry_fg_r.get()),
            int(entry_fg_g.get()),
            int(entry_fg_b.get())
        )
        bg = (
            int(entry_bg_r.get()),
            int(entry_bg_g.get()),
            int(entry_bg_b.get())
        )

        pattern = pattern_var.get()

        img = Image.new("RGB", (width, height), bg)
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                if pattern == "棋盘格":
                    if ((x // block) + (y // block)) % 2 == 0:
                        pixels[x, y] = fg
                elif pattern == "横条纹":
                    if (y // block) % 2 == 0:
                        pixels[x, y] = fg
                elif pattern == "纵条纹":
                    if (x // block) % 2 == 0:
                        pixels[x, y] = fg

        current_image = img
        show_image(img)

    except ValueError:
        pass


def show_image(img):
    preview = img.copy()
    preview.thumbnail((300, 300))
    tk_img = ImageTk.PhotoImage(preview)
    image_label.config(image=tk_img)
    image_label.image = tk_img


def save_image():
    if current_image is None:
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".bmp",
        filetypes=[("BMP Image", "*.bmp")]
    )
    if path:
        current_image.save(path, format="BMP")


# ================= GUI =================
root = tk.Tk()
root.title("图案生成器（BMP）")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# 尺寸
tk.Label(frame, text="宽(px)").grid(row=0, column=0)
entry_width = tk.Entry(frame, width=8)
entry_width.insert(0, "256")
entry_width.grid(row=0, column=1)

tk.Label(frame, text="高(px)").grid(row=0, column=2)
entry_height = tk.Entry(frame, width=8)
entry_height.insert(0, "256")
entry_height.grid(row=0, column=3)

# 块宽度 & 类型
tk.Label(frame, text="块宽").grid(row=1, column=0)
entry_block = tk.Entry(frame, width=8)
entry_block.insert(0, "32")
entry_block.grid(row=1, column=1)

tk.Label(frame, text="图案").grid(row=1, column=2)
pattern_var = tk.StringVar(value="棋盘格")
pattern_menu = ttk.Combobox(
    frame,
    textvariable=pattern_var,
    values=["棋盘格", "横条纹", "纵条纹"],
    state="readonly",
    width=10
)
pattern_menu.grid(row=1, column=3)

# 前景色
tk.Label(frame, text="前景 RGB").grid(row=2, column=0)
entry_fg_r = tk.Entry(frame, width=4)
entry_fg_g = tk.Entry(frame, width=4)
entry_fg_b = tk.Entry(frame, width=4)
entry_fg_r.insert(0, "255")
entry_fg_g.insert(0, "255")
entry_fg_b.insert(0, "255")
entry_fg_r.grid(row=2, column=1)
entry_fg_g.grid(row=2, column=2)
entry_fg_b.grid(row=2, column=3)

# 背景色
tk.Label(frame, text="背景 RGB").grid(row=3, column=0)
entry_bg_r = tk.Entry(frame, width=4)
entry_bg_g = tk.Entry(frame, width=4)
entry_bg_b = tk.Entry(frame, width=4)
entry_bg_r.insert(0, "0")
entry_bg_g.insert(0, "0")
entry_bg_b.insert(0, "0")
entry_bg_r.grid(row=3, column=1)
entry_bg_g.grid(row=3, column=2)
entry_bg_b.grid(row=3, column=3)

# 按钮
btn_frame = tk.Frame(root)
btn_frame.pack(pady=6)

tk.Button(btn_frame, text="手动生成", command=generate_image).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="保存 BMP", command=save_image).pack(side=tk.LEFT, padx=5)

# 预览
image_label = tk.Label(root)
image_label.pack(pady=10)

# ========= 实时预览绑定 =========
entries = [
    entry_width, entry_height, entry_block,
    entry_fg_r, entry_fg_g, entry_fg_b,
    entry_bg_r, entry_bg_g, entry_bg_b
]
for e in entries:
    e.bind("<KeyRelease>", generate_image)

pattern_menu.bind("<<ComboboxSelected>>", generate_image)

# 初始生成
generate_image()

root.mainloop()
