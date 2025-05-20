#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int fx(int x) {
    if (x == 1)
        return 1;
    return x * fx(x - 1);
}

int fy(int y) {
    if (y == 1 || y == 2)
        return 1;
    return fy(y - 1) + fy(y - 2);
}

int main() {
    int fd[2];
    if (pipe(fd) == -1) {
        perror("pipe");
        exit(1);
    }

    pid_t pid_fx, pid_fy;
    int x, y;
    printf("Input x and y:\n");
    scanf("%d %d", &x, &y);

    // 创建第一个子进程计算 f(x)
    pid_fx = fork();
    if (pid_fx == 0) {
        close(fd[0]); // 关闭管道读端
        printf("f(x) = %d\n", fx(x));
        write(fd[1], &fx(x), sizeof(fx(x))); // 将 f(x) 的结果写入管道
        close(fd[1]); // 关闭管道写端
        exit(0);
    }

    // 创建第二个子进程计算 f(y)
    pid_fy = fork();
    if (pid_fy == 0) {
        close(fd[0]); // 关闭管道读端
        printf("f(y) = %d\n", fy(y));
        write(fd[1], &fy(y), sizeof(fy(y))); // 将 f(y) 的结果写入管道
        close(fd[1]); // 关闭管道写端
        exit(0);
    }

    close(fd[1]); // 父进程关闭管道写端
    wait(NULL);
    wait(NULL);

    int result_x, result_y;
    read(fd[0], &result_x, sizeof(result_x)); // 从管道读取 f(x) 的结果
    read(fd[0], &result_y, sizeof(result_y)); // 从管道读取 f(y) 的结果
    printf("f(x, y) = %d\n", result_x + result_y);

    close(fd[0]); // 关闭管道读端

    return 0;
}
