#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define BROADCAST_PORT 5000
#define BROADCAST_IP "255.255.255.255"
#define BUFFER_SIZE 1024
#define MESSAGE_ID 100
#define LOCATION "C7"

typedef struct {
    int message_id;
    char location[100];
} hello_file;

void* send_to_client(void* arg) {
    int sock;
    struct sockaddr_in broadcast_addr;
    int broadcast_permission = 1;
    hello_file hello_message;

    // Tạo UDP socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Cấu hình socket cho phép broadcast
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast_permission, sizeof(broadcast_permission)) < 0) {
        perror("setsockopt failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Cấu hình địa chỉ broadcast
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(BROADCAST_PORT);
    broadcast_addr.sin_addr.s_addr = inet_addr(BROADCAST_IP);

    while (1) {
        // Chờ 8 giây
        sleep(8);

        // Tạo thông điệp MIB
        hello_message.message_id = MESSAGE_ID;
        strcpy(hello_message.location, LOCATION); // Sử dụng strcpy để gán chuỗi

        // Gửi thông điệp broadcast
        if (sendto(sock, &hello_message, sizeof(hello_message), 0, (struct sockaddr*)&broadcast_addr, sizeof(broadcast_addr)) < 0) {
            perror("sendto failed");
            close(sock);
            exit(EXIT_FAILURE);
        }

        printf("Broadcasted: message id = %d, location = %s\n", hello_message.message_id, hello_message.location);
    }

    close(sock);
    return NULL;
}

int main() {
    pthread_t broadcast_thread;

    // Tạo một luồng cho việc broadcast
    if (pthread_create(&broadcast_thread, NULL, send_to_client, NULL) != 0) {
        perror("Failed to create broadcast thread");
        exit(EXIT_FAILURE);
    }

    // Đợi các luồng hoàn thành (sẽ không bao giờ hoàn thành vì luồng chạy vô hạn)
    pthread_join(broadcast_thread, NULL);

    return 0;
}









