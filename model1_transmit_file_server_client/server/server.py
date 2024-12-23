import socket
import threading
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, END
import os

SERVER_IP = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024
SAVE_DIR_SERVER = "./server/received_files"

# Đường dẫn assets của Tkinter Designer
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\trap\Idiot Huster\20241_Mạng máy tính\programming\Tkinter-Designer-master\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Hàm khởi động server
def start_server(text_widget):
    if not os.path.exists(SAVE_DIR_SERVER):
        os.makedirs(SAVE_DIR_SERVER)

    def server_logic():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_IP, PORT))
            server_socket.listen(5)
            text_widget.insert(END, "Server is listening...\n")

            while True:
                client_socket, client_addr = server_socket.accept()
                text_widget.insert(END, f"Client {client_addr} connected.\n")
                threading.Thread(target=handle_client, args=(client_socket, text_widget)).start()

    def handle_client(client_socket, text_widget):
        with client_socket:
            while True:
                file_name = client_socket.recv(BUFFER_SIZE).decode()
                if not file_name:
                    break
                text_widget.insert(END, f"Receiving file: {file_name}\n")
                with open(os.path.join(SAVE_DIR_SERVER, file_name), "wb") as file:
                    while True:
                        data = client_socket.recv(BUFFER_SIZE)
                        if not data:
                            break
                        file.write(data)
                text_widget.insert(END, f"File {file_name} received successfully by server.\n")

    threading.Thread(target=server_logic, daemon=True).start()


# Giao diện chính
# Giao diện GUI
root = Tk()
root.title("File Transfer - Server")
text = Text(root, height=20, width=50)
text.pack()
start_button = Button(root, text="Start Server", command=lambda: start_server(text))
start_button.pack()
root.mainloop()  