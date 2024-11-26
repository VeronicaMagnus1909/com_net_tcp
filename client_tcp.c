#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "127.0.0.1"  // Địa chỉ IP của server (localhost trong ví dụ này)
#define SERVER_PORT 5000
#define BUFFER_SIZE 1024

int main() {
    int sock;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];

    // Tạo socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Cấu hình địa chỉ và cổng cho server
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);

    // Chuyển đổi địa chỉ IP sang dạng mạng
    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("Invalid address");
        exit(EXIT_FAILURE);
    }

    // Kết nối tới server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connection failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    printf("Connected to server\n");

    // Gửi và nhận dữ liệu với server
    while (1) {
        printf("Enter message: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0;  // Xóa ký tự newline

        // Gửi dữ liệu tới server
        send(sock, buffer, strlen(buffer), 0);

        // Nhận dữ liệu từ server
        int bytes_received = recv(sock, buffer, BUFFER_SIZE, 0);
        if (bytes_received <= 0) {
            if (bytes_received == 0) {
                printf("Server disconnected\n");
            } else {
                perror("Recv failed");
            }
            break;
        }

        buffer[bytes_received] = '\0';  // Đảm bảo chuỗi kết thúc
        printf("Received from server: %s\n", buffer);
    }

    // Đóng kết nối
    close(sock);
    return 0;
}
