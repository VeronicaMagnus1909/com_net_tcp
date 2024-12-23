#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define SERVER_IP "127.0.0.1"
#define PORT 5000
#define BUFFER_SIZE 1024

void* receive_handler(void* socket_desc) {
    int sock = *(int*)socket_desc;
    char buffer[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        // Nhận dữ liệu từ server
        int bytes_received = recv(sock, buffer, BUFFER_SIZE, 0);
        if (bytes_received <= 0) {
            printf("Server disconnected.\n");
            break;
        }
        printf("Server: %s\n", buffer);
    }
    close(sock);
    return NULL;
}

void* send_handler(void* socket_desc) {
    int sock = *(int*)socket_desc;
    char buffer[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        printf("Client: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        // Gửi dữ liệu tới server
        if (send(sock, buffer, strlen(buffer), 0) <= 0) {
            printf("Failed to send message.\n");
            break;
        }
    }
    close(sock);
    return NULL;
}

int main() {
    int sock;
    struct sockaddr_in server_addr;
    pthread_t recv_thread, send_thread;

    // Tạo socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Cấu hình địa chỉ server
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("Invalid server IP address");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Kết nối tới server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection to server failed");
        close(sock);
        exit(EXIT_FAILURE);
    }
    printf("Connected to server.\n");

    int* new_sock = malloc(sizeof(int));
    *new_sock = sock;

    // Tạo thread nhận và gửi dữ liệu
    pthread_create(&recv_thread, NULL, receive_handler, (void*)new_sock);
    pthread_create(&send_thread, NULL, send_handler, (void*)new_sock);

    // Chờ các thread kết thúc
    pthread_join(recv_thread, NULL);
    pthread_join(send_thread, NULL);

    close(sock);
    return 0;
}





