import socket
from tkinter import Tk, Button, Label, filedialog, Text, END

SERVER_IP = "127.0.0.1"  # Địa chỉ IP của server
PORT = 5000
BUFFER_SIZE = 1024


def send_file(file_path, text_widget):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, PORT))
            file_name = file_path.split("/")[-1]

            # Gửi tên file
            client_socket.send(file_name.encode())

            # Gửi dữ liệu file
            with open(file_path, "rb") as file:
                chunk = file.read(BUFFER_SIZE)
                while chunk:
                # Xử lý chunk
                    chunk = file.read(BUFFER_SIZE)

                
                    client_socket.send(chunk)

            text_widget.insert(END, f"File {file_name} sent successfully.\n")
    except Exception as e:
        text_widget.insert(END, f"Error: {str(e)}\n")


def select_file(text_widget):
    file_path = filedialog.askopenfilename()
    if file_path:
        text_widget.insert(END, f"Selected file: {file_path}\n")
        send_file(file_path, text_widget)


# Giao diện GUI
root = Tk()
root.title("File Transfer - Client")
text = Text(root, height=20, width=50)
text.pack()
select_button = Button(root, text="Select File", command=lambda: select_file(text))
select_button.pack()
root.mainloop()
