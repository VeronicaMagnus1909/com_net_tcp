import os
import socket
import threading
from tkinter import *
from tkinter import filedialog, messagebox


class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat & Transfer App")
        self.master.geometry("600x400")
        self.server_socket = None
        self.client_name = None
        self.chat_windows = {}  # Lưu trữ cửa sổ chat với các client khác
        self.logs = []  # Danh sách log

        # GUI chính
        self.label_name = Label(master, text="Tên của bạn:", font=("Arial", 12))
        self.label_name.pack(pady=5)

        self.entry_name = Entry(master, font=("Arial", 12), width=30)
        self.entry_name.pack(pady=5)

        self.btn_connect = Button(
            master, text="Kết nối", font=("Arial", 12), command=self.connect_to_server
        )
        self.btn_connect.pack(pady=10)

        self.label_clients = Label(master, text="Danh sách client:", font=("Arial", 12))
        self.label_clients.pack(pady=5)

        self.list_clients = Listbox(master, font=("Arial", 12), height=10, width=50)
        self.list_clients.bind(
            "<Double-1>", self.open_chat_window
        )  # Nhấp đúp để mở cửa sổ chat
        self.list_clients.pack(pady=5)

        self.label_status = Label(
            master, text="Trạng thái: Chưa kết nối", font=("Arial", 12)
        )
        self.label_status.pack(pady=10)

    # kết nối với server bằng việc ấn 
    def connect_to_server(self):
        self.client_name = self.entry_name.get()
        if not self.client_name:
            self.label_status.config(text="Vui lòng nhập tên trước khi kết nối.")
            return

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect(("127.0.0.1", 12345))
            self.server_socket.send(self.client_name.encode("utf-8"))
            threading.Thread(target=self.listen_to_server, daemon=True).start()
            self.label_status.config(text="Đã kết nối với server.")
        except Exception as e:
            self.label_status.config(text=f"Không thể kết nối: {e}")
    # Luôn lắng nghe server -> use While true
    def listen_to_server(self):
        while True:
            try:
                # data is important (start with message or file or client_list)
                data = self.server_socket.recv(1024).decode("utf-8")
                if data.startswith("MESSAGE"):
                    _, sender, message = data.split("||")
                    self.handle_received_message(sender, message)
                elif data.startswith("FILE"):
                    _, sender, file_name = data.split("||")
                    self.handle_received_file(sender, file_name)
                elif data.startswith("CLIENT_LIST"):
                    _, client_list = data.split("||")
                    all_clients = client_list.split(",")
                    self.client_list = [
                        client for client in all_clients if client != self.client_name
                    ]
                    self.update_client_list()
            except Exception as e:
                self.label_status.config(text=f"Lỗi: {e}")
                break
    
    # upadate list client, who is online right now
    def update_client_list(self):
        self.list_clients.delete(0, END)
        for client in self.client_list:
            self.list_clients.insert(END, client)
    
    #
    def open_chat_window(self, event):
        selected_client = self.list_clients.get(ACTIVE)
        if selected_client:
            self.create_chat_window(selected_client)

    def handle_received_message(self, sender, message):
        # In tin nhắn ra console để kiểm tra
        print(f"Tin nhắn nhận được từ {sender}: {message}")

        # Hiển thị tin nhắn trong cửa sổ chat nếu đã tồn tại
        if sender not in self.chat_windows:
            self.create_chat_window(sender)
        chat_window = self.chat_windows[sender]
        chat_textbox = chat_window["textbox"]
        chat_textbox.insert(END, f"{sender}: {message}\n")
        self.logs.append(f"RECEIVED from {sender}: {message}")

    def handle_received_file(self, sender, file_name):
        # Tạo thư mục cho client nếu chưa tồn tại
        client_folder = f"./{self.client_name}"
        if not os.path.exists(client_folder):
            os.makedirs(client_folder)

        # Nhận kích thước file
        file_size = int(self.server_socket.recv(1024).decode("utf-8"))
        file_path = os.path.join(client_folder, file_name)

        print(f"[INFO] Đang nhận file '{file_name}' ({file_size} bytes) từ {sender}...")

        # Ghi file nhị phân
        received = 0
        try:
            with open(file_path, "wb") as f:
                while received < file_size:
                    chunk = self.server_socket.recv(4096)
                    if not chunk:
                        break  # Dừng nếu không nhận thêm dữ liệu
                    f.write(chunk)
                    received += len(chunk)
                    print(f"[INFO] Đã nhận được {received}/{file_size} bytes")

            # Log kết quả
            if received == file_size:
                print(f"[SUCCESS] File '{file_name}' đã được lưu vào {file_path}")
                if sender in self.chat_windows:
                    chat_window = self.chat_windows[sender]["textbox"]
                    chat_window.insert(
                        END,
                        f"Đã nhận file '{file_name}' từ {sender}. File lưu tại: {file_path}\n",
                    )
            else:
                print(
                    f"[ERROR] File nhận không đầy đủ. Nhận {received}/{file_size} bytes"
                )
        except Exception as e:
            print(f"[ERROR] Lỗi khi nhận file '{file_name}': {e}")

    def create_chat_window(self, client_name):
        if client_name in self.chat_windows:
            return
        window = Toplevel(self.master)
        window.title(f"Chat với {client_name}")
        window.geometry("400x400")

        frame_top = Frame(window)
        frame_top.pack(pady=10)

        textbox = Text(frame_top, font=("Arial", 12), height=15, width=40)
        textbox.pack()

        frame_bottom = Frame(window)
        frame_bottom.pack(pady=5)

        entry_message = Entry(frame_bottom, font=("Arial", 12), width=25)
        entry_message.grid(row=0, column=0, padx=5)

        btn_send_message = Button(
            frame_bottom,
            text="Gửi tin nhắn",
            font=("Arial", 12),
            command=lambda: self.send_message(client_name, entry_message, textbox),
        )
        btn_send_message.grid(row=0, column=1, padx=5)

        btn_send_file = Button(
            frame_bottom,
            text="Gửi file",
            font=("Arial", 12),
            command=lambda: self.send_file(client_name, textbox),
        )
        btn_send_file.grid(row=1, column=0, columnspan=2, pady=10)

        self.chat_windows[client_name] = {"window": window, "textbox": textbox}

    def send_message(self, target_client, entry_message, chat_textbox):
        message = entry_message.get()
        if message:
            try:
                self.server_socket.send(
                    f"MESSAGE||{target_client}||{message}".encode("utf-8")
                )
                chat_textbox.insert(END, f"Bạn: {message}\n")
                entry_message.delete(0, END)
                self.logs.append(f"SENT to {target_client}: {message}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể gửi tin nhắn: {e}")

    def send_file(self, target_client, chat_textbox):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        try:
            # Gửi lệnh và thông tin file
            self.server_socket.send(
                f"SEND_FILE||{target_client}||{file_name}".encode("utf-8")
            )
            self.server_socket.send(
                str(file_size).encode("utf-8")
            )  # Gửi kích thước file
            print(f"[INFO] Đang gửi file '{file_name}' ({file_size} bytes)...")

            # Gửi file nhị phân
            with open(file_path, "rb") as f:
                sent = 0
                while chunk := f.read(4096):
                    self.server_socket.send(chunk)
                    sent += len(chunk)
                    print(f"[INFO] Đã gửi {sent}/{file_size} bytes")

            chat_textbox.insert(END, f"Bạn đã gửi file: {file_name}\n")
            print(f"[SUCCESS] File '{file_name}' đã được gửi thành công.")
        except Exception as e:
            print(f"[ERROR] Lỗi khi gửi file: {e}")

    def show_logs(self):
        log_window = Toplevel(self.master)
        log_window.title("Logs")
        log_window.geometry("400x300")

        log_textbox = Text(log_window, font=("Arial", 12), height=15, width=40)
        log_textbox.pack(pady=5)

        for log in self.logs:
            log_textbox.insert(END, log + "\n")


root = Tk()
app = ClientApp(root)
root.mainloop()
