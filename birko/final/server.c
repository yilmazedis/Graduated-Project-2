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
#include "myStack.h"
#include <stdbool.h>
#include <dirent.h>

#define FILE_NAME_SIZE 20
#define MAX_DIR 10
#define MAX_FILE_SIZE 1024 // 1KB
#define MAX_FILE 10

struct StackNode* root = NULL; 

pthread_mutex_t lock; 
sem_t sem;
int threadPoolSize = 50;
int flag = 0;
int threadFlag = 0;
int thi, thj;
bool stop = false;
char requiredDir[MAX_DIR];

int id;
int fd;
int welcomeSocket;
struct sockaddr_in serverAddr;
struct sockaddr_in serverStorage;
socklen_t addr_size;

typedef struct{
    pthread_t tid; // thread ID'si
    int clientSocket;
}threadStruct;

typedef struct{
    char filename[FILE_NAME_SIZE];
    char data[MAX_FILE_SIZE];
    long len;

    char status;
    bool visited;
    bool isdel;
}File_t;

typedef struct
{
	int idle;
}Idle_t;

Idle_t idle;

typedef struct
{
	File_t file[MAX_FILE];
	int size;

	bool ctrlc;
}Folder_t;

threadStruct dataOfThreads[255];

char* readFileBytes(const char *name, long *lenf);
void writeFileBytes(const char *name, char* data, long lenf);
void *threadPool();
void catchctrlc(int signo);
void showFiles(Folder_t folder);
void writeFolder(Folder_t folder);
void removeDeletedFiles(Folder_t folder);
void removeFile(char * filename);

int main(int argc,char **argv){

	int socketget;
	struct sigaction act;
    act.sa_handler = catchctrlc;
    act.sa_flags = 0;
    int i =0,j=0;
    int c;

    idle.idle = -1;


   	if (argc != 4)
	{
		printf("usage : ./server <dir> <thread pool size> <port: 8080>\n");
		exit(1);
	}

	if (pthread_mutex_init(&lock, NULL) != 0) 
    { 
        printf("\n mutex init has failed\n"); 
        return 1; 
    } 

	threadPoolSize = atoi(argv[2]);
	printf("%d\n", threadPoolSize);
	sprintf(requiredDir,"%s",argv[1]);
	sem_init(&sem, 0, 0);

	welcomeSocket = socket(PF_INET, SOCK_STREAM, 0);


    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(atoi(argv[3]));
    serverAddr.sin_addr.s_addr =inet_addr("127.0.0.1");
    memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

    /*---- Bind the address struct to the socket ----*/
    bind(welcomeSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));



    if ((sigemptyset(&act.sa_mask) == -1) || (sigaction(SIGINT, &act, NULL) == -1))
        perror("Failed to set SIGINT to handle Ctrl-C");

    /*---- Listen on the socket, with 5 max connection requests queued ----*/
    if(listen(welcomeSocket,100)!=0){
    	perror("listen ");
    }

    for (i = 0; i < threadPoolSize; ++i)
    {
        pthread_create(&(dataOfThreads[i].tid),NULL,threadPool,NULL);
    }


    /*---- Accept call creates a new socket for the incoming connection ----*/
    addr_size = sizeof(serverStorage);

    for (thi = 0; thi < threadPoolSize; ++i)
    {
       socketget = accept(welcomeSocket, (struct sockaddr *) &serverStorage, &addr_size);
       push(&root, socketget); 
       sem_post(&sem);
    }
    

    for(thj=0;thj<threadPoolSize;++thj){
        pthread_join((dataOfThreads[thj].tid),NULL);
    }

    close(welcomeSocket);
    
    return 0;
}

void catchctrlc(int signo) {

    fprintf(stderr, " Ctrl-C has Occurred. All Threads KILLED\n");

    threadFlag = 1;
    stop = true;
    
    while(thi < threadPoolSize) {
        sem_post(&sem);
        thi++;
    }

    while(thj<threadPoolSize) {
        pthread_join((dataOfThreads[thj].tid),NULL);
        thj++;
    }
    
    exit(0);  
}

void *threadPool(){

	int socketID;
	Folder_t folder;

    //wait 
    sem_wait(&sem);



    if (!isEmpty(root)) {
    	socketID = pop(&root);

    	fprintf(stderr, "%d popped from stack\n", socketID); 
    }

    if (threadFlag == 0) {
    	while(!stop) {
    		pthread_mutex_lock(&lock); 
	        printf("\nEntered..\n");

	        read(socketID,&folder,sizeof(Folder_t));

	        //printf("size %s\n", folder.file[0].filename);
	        
	        removeDeletedFiles(folder);

		    showFiles(folder);

		    writeFolder(folder);

		    
		    
		    //writeFileBytes("./serverDir/osmanKro.pdf", fileInfo.data, fileInfo.len);
		    sleep(1);
		    printf("End Of Server\n");
		    pthread_mutex_unlock(&lock);
	       
	        //signal 
	        printf("\nJust Exiting...\n");

	        write(socketID,&idle,sizeof(Idle_t));
    	}
    }
   
    pthread_exit(0);
}

char* readFileBytes(const char *name, long *lenf)  
{  
    FILE *fl = fopen(name, "r"); 
    fseek(fl, 0, SEEK_END);  
    long len = ftell(fl);  
    char *ret = malloc(len);  
    fseek(fl, 0, SEEK_SET);  
    fread(ret, 1, len, fl);  
    fclose(fl);

    *lenf = len;
    return ret;  
}

void removeDeletedFiles(Folder_t folder) {

	int i;
	char cwd[PATH_MAX];
	char newfile[PATH_MAX];


	getcwd(cwd, sizeof(cwd));
	//chdir(requiredDir);

	sprintf(cwd, "%s/%s", cwd, requiredDir);
    

	for (i = 0; i < folder.size; ++i)
	{
		if (folder.file[i].status == 'D' && folder.file[i].isdel == false)
        {
        	sprintf(newfile, "%s/%s", cwd, folder.file[i].filename);
        	removeFile(newfile);
        	idle.idle = i;
        	newfile[0] = '\0';
        }
	}
}

void removeFile(char * filename) {

	int status;

	status = remove(filename);

	if (status == 0)
		printf("%s file deleted successfully.\n",filename);
	else
	{
		printf("Unable to delete the file\n");
		perror("Following error occurred");
	}
}

void writeFileBytes(const char *name, char* data, long lenf)  
{  
    FILE *fl = fopen(name, "wb");  
    
    fwrite(data, lenf, 1, fl);
    fclose(fl);

    return;  
} 

void showFiles(Folder_t folder){

    for (int i = 0; i < folder.size; ++i)
    {
        if (folder.file[i].status != 'D')
        {
            fprintf(stderr,"%s %c\n",folder.file[i].filename, folder.file[i].status);
        }
    }
}

void writeFolder(Folder_t folder){
	
	int i, j;
	char* data;
	char cwd[PATH_MAX];
	char newfile[PATH_MAX];


	getcwd(cwd, sizeof(cwd));
	//chdir(requiredDir);

	sprintf(cwd, "%s/%s", cwd, requiredDir);

	for (i = 0; i < folder.size; ++i)
	{	
		if (folder.file[i].status != 'D')
        {	
        	sprintf(newfile, "%s/%s", cwd, folder.file[i].filename);
	    	writeFileBytes(newfile, folder.file[i].data , folder.file[i].len);
	    	newfile[0] = '\0';
    	}
	}
}