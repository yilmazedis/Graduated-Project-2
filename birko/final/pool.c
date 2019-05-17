#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <semaphore.h>
#include <pthread.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>

sem_t sem;
int count = 50;
int flag = 0;
int threadFlag = 0;
int thi, thj;

typedef struct{
    pthread_t tid; // thread ID'si
    int clientSocket;
}threadStruct;


threadStruct dataOfThreads[255];

void catchctrlc(int signo) {

    fprintf(stderr, "Ctrl-C has Occurred. All Threads KILLED\n");

    threadFlag = 1;
    
    while(thi < count) {
        sem_post(&sem);
        thi++;
    }

    while(thj<count) {
        pthread_join((dataOfThreads[thj].tid),NULL);
        thj++;
    }
    
    exit(0);  
}

void *threadPool(void *a){

    //wait 
    sem_wait(&sem);
    
    if (threadFlag == 0) {
        printf("\nEntered..\n"); 
       
        //signal 
        printf("\nJust Exiting...\n");
    }
    
    pthread_exit(0);
}


int main(int argc,char **argv){

    struct sigaction act;
    act.sa_handler = catchctrlc;
    act.sa_flags = 0;
    int i =0,j=0;
    int c;

    sem_init(&sem, 0, 1);

    if ((sigemptyset(&act.sa_mask) == -1) || (sigaction(SIGINT, &act, NULL) == -1))
        perror("Failed to set SIGINT to handle Ctrl-C");

    for (i = 0; i < count; ++i)
    {
        pthread_create(&(dataOfThreads[i].tid),NULL,threadPool,NULL);
    }

    printf("All Thread Ready\n");

    for (thi = 0; thi < count; ++i)
    {
       scanf("%d",&c);
       sem_post(&sem);
    }

    for(thj=0;thj<count;++thj){
        pthread_join((dataOfThreads[thj].tid),NULL);
    }

    return 0;
}
