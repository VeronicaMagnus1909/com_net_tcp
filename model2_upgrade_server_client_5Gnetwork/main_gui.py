import os
from pathlib import Path
import subprocess
from tkinter import messagebox

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\trap\Idiot Huster\20241_Mạng máy tính\programming\project4\assets\frame0")

### Define function
current_dir = os.path.dirname(os.path.abspath(__file__))

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_client_file(event):
    try:
        # Đường dẫn tương đối đến client.py
        client_path = os.path.join(current_dir, "client.py")
        subprocess.Popen(["python", client_path])
        messagebox.showinfo("Thông báo", "Client đã được khởi chạy!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi chạy client: {e}")

def open_server_file(event):
    try:
        # Đường dẫn tương đối đến server.py
        server_path = os.path.join(current_dir, "server.py")
        subprocess.Popen(["python", server_path])
        messagebox.showinfo("Thông báo", "Server đã được khởi chạy!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi chạy server: {e}")

def open_core_file(event):
    try:
        # Đường dẫn tương đối đến server.py
        server_path = os.path.join(current_dir, "core.py")
        subprocess.Popen(["python", server_path])
        messagebox.showinfo("Thông báo", "Core đã được khởi chạy!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi chạy core: {e}")



window = Tk()

window.geometry("985x577")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 577,
    width = 985,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    176.0,
    41.0,
    826.0,
    82.0,
    fill="#5475D6",
    outline="")

canvas.create_rectangle(
    335.0,
    106.0,
    653.0,
    204.0,
    fill="#748DD6",
    outline="")

canvas.create_text(
    350.0,
    116.0,
    anchor="nw",
    text="Status: \nUser src: \nUser dest:\nFile name:\nFile size:\n",
    fill="#000000",
    font=("Inter SemiBold", 13 * -1)
)

canvas.create_text(
    335.0,
    50.0,
    anchor="nw",
    text="Simulation file transmission in 5G network",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_rectangle(
    89.0,
    505.0,
    184.0,
    536.0,
    fill="#55DFE6",
    outline="")

canvas.create_text(
    125.0,
    511.0,
    anchor="nw",
    text="UE",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_rectangle(
    240.0,
    386.0,
    335.0,
    417.0,
    fill="#329ADB",
    outline="")

canvas.create_text(
    257.0,
    392.0,
    anchor="nw",
    text="gnodeB",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_rectangle(
    636.0,
    380.0,
    731.0,
    411.0,
    fill="#329ADB",
    outline="")

canvas.create_rectangle(
    422.0,
    417.0,
    553.0,
    461.0,
    fill="#0C66C0",
    outline="")

canvas.create_text(
    653.0,
    386.0,
    anchor="nw",
    text="GnodeB",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_text(
    436.0,
    429.0,
    anchor="nw",
    text="core network",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_rectangle(
    801.0,
    499.0,
    896.0,
    530.0,
    fill="#55DFE6",
    outline="")

canvas.create_text(
    837.0,
    505.0,
    anchor="nw",
    text="UE",
    fill="#F5F5F5",
    font=("Inter SemiBold", 16 * -1)
)

### Images 
# 1,2,3,4,5,6: UE
# 7,8: gnobe
# 9: core

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    136.0,
    204.0,
    image=image_image_1
)



image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    136.0,
    320.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    137.0,
    433.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    848.0,
    204.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    845.0,
    317.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    846.0,
    429.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    291.0,
    304.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    693.0,
    304.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    489.0,
    318.0,
    image=image_image_9
)

# Thêm hình ảnh và sự kiện
### Hình ảnh và sự kiện click
# Các hình ảnh liên quan đến client
for img_name in ["image_1.png", "image_2.png", "image_3.png", "image_4.png", "image_5.png", "image_6.png"]:
    image = PhotoImage(file=relative_to_assets(img_name))
    img_item = canvas.create_image(136.0, 204.0, image=image)
    canvas.tag_bind(img_item, "<Button-1>", open_client_file)

# Các hình ảnh liên quan đến server
for img_name in ["image_7.png", "image_8.png"]:
    image = PhotoImage(file=relative_to_assets(img_name))
    img_item = canvas.create_image(291.0, 304.0, image=image)
    canvas.tag_bind(img_item, "<Button-1>", open_server_file)

# Hình ảnh liên quan đến core
image_core = PhotoImage(file=relative_to_assets("image_9.png"))
img_core = canvas.create_image(489.0, 318.0, image=image_core)
canvas.tag_bind(img_core, "<Button-1>", open_core_file)


window.resizable(False, False)
window.mainloop()
