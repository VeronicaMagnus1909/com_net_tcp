import os
import socket
import threading

# Danh sách client kết nối
clients = {}


# Gửi cho tất cả các client list những client đang onl
def broadcast_client_list():
    """Gửi danh sách client đến tất cả các client đã kết nối."""
    client_list = ",".join(clients.keys())
    for client_socket in clients.values():
        client_socket.send(f"CLIENT_LIST||{client_list}".encode("utf-8"))


def handle_client(client_socket, client_address):
    try:
        client_name = client_socket.recv(1024).decode("utf-8")
        clients[client_name] = client_socket
        print(f"[+] {client_name} đã kết nối từ {client_address}")

        broadcast_client_list()

        while True:
            data = client_socket.recv(1024).decode("utf-8", errors="ignore")
            if not data:
                break

            # Xử lý gửi file
            if data.startswith("SEND_FILE"):
                try:
                    _, target_client, file_name = data.split("||")
                    print(
                        f"[SEND_FILE] {client_name} gửi file '{file_name}' đến {target_client}"
                    )
                    if target_client in clients:
                        clients[target_client].send(
                            f"FILE||{client_name}||{file_name}".encode("utf-8")
                        )
                        # Nhận kích thước file
                        file_size_data = (
                            client_socket.recv(1024).decode("utf-8").strip()
                        )
                        if not file_size_data.isdigit():
                            print(
                                f"[ERROR] Kích thước file không hợp lệ: {file_size_data}"
                            )
                            continue

                        file_size = int(file_size_data)
                        clients[target_client].send(str(file_size).encode("utf-8"))
                        print(f"[INFO] Kích thước file: {file_size} bytes")

                        # Gửi file theo dạng nhị phân
                        received = 0
                        while received < file_size:
                            chunk = client_socket.recv(4096)
                            if not chunk:
                                break
                            received += len(chunk)
                            clients[target_client].send(chunk)
                        print(
                            f"[SUCCESS] File '{file_name}' đã được gửi đến {target_client}"
                        )
                    else:
                        client_socket.send(
                            "ERROR||Client không tồn tại".encode("utf-8")
                        )
                except Exception as e:
                    print(f"[ERROR] Lỗi xử lý file: {e}")

            # Xử lý tin nhắn
            elif data.startswith("MESSAGE"):
                _, target_client, message = data.split("||", 2)
                if target_client in clients:
                    clients[target_client].send(
                        f"MESSAGE||{client_name}||{message}".encode("utf-8")
                    )
                else:
                    print(f"[ERROR] {target_client} không tồn tại.")
    except Exception as e:
        print(f"[-] Lỗi từ {client_address}: {e}")
    finally:
        if client_name in clients:
            del clients[client_name]
        broadcast_client_list()
        client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(5)
print("[+] Server đang chạy...")

while True:
    client_socket, client_address = server.accept()
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
