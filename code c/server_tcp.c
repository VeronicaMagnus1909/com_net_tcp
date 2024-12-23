#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define PORT 5000
#define BUFFER_SIZE 1024

void* receive_handler(void* socket_desc) {
    int client_sock = *(int*)socket_desc;
    char buffer[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        // Nhận dữ liệu từ client
        int bytes_received = recv(client_sock, buffer, BUFFER_SIZE, 0);
        if (bytes_received <= 0) {
            printf("Client disconnected.\n");
            break;
        }
        printf("Client: %s\n", buffer);
    }
    close(client_sock);
    free(socket_desc);
    return NULL;
}

void* send_handler(void* socket_desc) {
    int client_sock = *(int*)socket_desc;
    char buffer[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        printf("Server: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        // Gửi dữ liệu tới client
        if (send(client_sock, buffer, strlen(buffer), 0) <= 0) {
            printf("Failed to send message.\n");
            break;
        }
    }
    close(client_sock);
    return NULL;
}

int main() {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    pthread_t recv_thread, send_thread;

    // Tạo socket
    if ((server_sock = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Cấu hình địa chỉ server
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Gắn socket vào địa chỉ
    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server_sock);
        exit(EXIT_FAILURE);
    }

    // Lắng nghe kết nối
    if (listen(server_sock, 1) < 0) {
        perror("Listen failed");
        close(server_sock);
        exit(EXIT_FAILURE);
    }
    printf("Server listening on port %d...\n", PORT);

    socklen_t addr_len = sizeof(client_addr);
    if ((client_sock = accept(server_sock, (struct sockaddr*)&client_addr, &addr_len)) < 0) {
        perror("Accept failed");
        close(server_sock);
        exit(EXIT_FAILURE);
    }
    printf("Client connected.\n");

    int* new_sock = malloc(sizeof(int));
    *new_sock = client_sock;

    // Tạo thread nhận và gửi dữ liệu
    pthread_create(&recv_thread, NULL, receive_handler, (void*)new_sock);
    pthread_create(&send_thread, NULL, send_handler, (void*)new_sock);

    // Chờ các thread kết thúc
    pthread_join(recv_thread, NULL);
    pthread_join(send_thread, NULL);

    close(server_sock);
    return 0;
}

