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
#include <time.h>
#include <stdbool.h>
#include <dirent.h>
#include <signal.h>

#define FILE_NAME_SIZE 20
#define MAX_DIR 10
#define MAX_FILE_SIZE 1024 // 1KB
#define MAX_FILE 10

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
	File_t file[MAX_FILE];
	int size;

	bool ctrlc;
}Folder_t;

typedef struct
{
	int idle;
}Idle_t;

Idle_t idle;
Folder_t folder;

typedef struct
{
	struct timespec lastModification;
}File_Last_Modification_t;

File_Last_Modification_t lastModi[MAX_FILE];

char requiredDir[MAX_DIR];
struct sockaddr_in serverAddr;
socklen_t addr_size;

bool stopWrite = false;

int clientSocket;


char* readFileBytes(const char *name, long *lenf);
void writeFileBytes(const char *name, char* data, long lenf);
void fillFolder();
void removeFile(char * filename);

void setVisitedFalse();
int isFileExist(char * filename);
void showFiles();
int checkFiles();
void setDeletedFiles();
int sendDataToServer();
void *checkerThread();

void catchctrlc(int signo);

int main(int argc,char **argv){

    long i,j;
    long len;
    char* data;
    pthread_t thCheck;
    struct sigaction act;
    act.sa_handler = catchctrlc;
    act.sa_flags = 0;

    folder.ctrlc = false;

    if (argc != 4)
	{
		printf("usage : ./client  <dirname> <port: 8080> <ip: 127.0.0.1> \n");
		exit(1);
	}

    if ((sigemptyset(&act.sa_mask) == -1) || (sigaction(SIGINT, &act, NULL) == -1))
    	perror("Failed to set SIGINT to handle Ctrl-C");

    // Initialize
    folder.size = 0;

	sprintf(requiredDir,"%s",argv[1]);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(atoi(argv[2]));
    serverAddr.sin_addr.s_addr = inet_addr(argv[3]);
    memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero); 

    clientSocket = socket(PF_INET, SOCK_STREAM, 0);
    addr_size = sizeof(serverAddr);
    
    if (connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size) == -1){
		perror("Connection Error");
    }else{
    	printf("Connection is successed\n");
    }

    ////////////////////////////////////////
    // Fill Struct Part

    
    

    ////////////////////////////////////////
    while(1) {
    	printf("---------------------\n");
	   	for (i = 0; i < 6; ++i)
	   	{
			checkFiles();
	    }

	    showFiles();
    
    	fillFolder();

    	write(clientSocket,&folder,sizeof(Folder_t));
    	read(clientSocket,&idle,sizeof(Idle_t));
    	folder.file[idle.idle].isdel = true;
    	printf("%d\n", folder.size);
	}

    printf("End Of Client\n");

    close(clientSocket);

    return 0;
}

void catchctrlc(int signo) {

    fprintf(stderr, " Ctrl-C has Occurred. All Threads KILLED\n");


    folder.ctrlc = true;
    write(clientSocket,&folder,sizeof(Folder_t));

    exit(0);  
}

void fillFolder() {

	int i, j;
	char* data;

	chdir(requiredDir);

	for (i = 0; i < folder.size; ++i)
	{	
		if (folder.file[i].status != 'D')
        {
			data = readFileBytes(folder.file[i].filename, &folder.file[i].len);
			
			for (j = 0; j < folder.file[i].len; ++j)	
	    		folder.file[i].data[j] = data[j];
    	}
	}
}

void setVisitedFalse(){

    for (int i = 0; i < MAX_FILE; ++i)
        folder.file[i].visited = false;
}

int isFileExist(char * filename){
    for (int i = 0; i < folder.size; ++i)
        if (strcmp(folder.file[i].filename,filename) == 0)
            return i;
    return -1;
}

void showFiles(){

    for (int i = 0; i < folder.size; ++i)
    {
        if (folder.file[i].status != 'D')
        {
            printf("%s %c\n",folder.file[i].filename, folder.file[i].status);
        }
    }
}

void setDeletedFiles(){
    for (int i = 0; i < folder.size; ++i)
    {
        if(folder.file[i].visited == false){
            folder.file[i].status = 'D';
            //printf("hi\n");
        }
    }
}

int checkFiles(){
    DIR *d;
    int index;
    struct dirent *dir;

    chdir(requiredDir);

    d = opendir(".");

    if (d)
    {   
        struct stat statOfFile;
        setVisitedFalse();
        while ((dir = readdir(d)) != NULL)
        {
            if (dir->d_name[0] != '.')
            {   
                if (lstat(dir->d_name, &statOfFile) == -1) {
                    perror("lstat");
                    exit(0);
                }
                index = isFileExist(dir->d_name);
                if(index == -1){
                    sprintf(folder.file[folder.size].filename,"%s",dir->d_name);
                    folder.file[folder.size].status = 'C';
                    folder.file[folder.size].visited = true;
                    lastModi[folder.size].lastModification = statOfFile.st_mtim;
                    folder.size++;
                    folder.file[idle.idle].isdel = false;
                }
                else{
                    if (lastModi[index].lastModification.tv_sec != statOfFile.st_mtime)
                    {
                        folder.file[index].status = 'M';                                // Modified
                        lastModi[index].lastModification = statOfFile.st_mtim;
                    }
                    else{
                        folder.file[index].status = 'U';                                // Unchanged
                    }
                    folder.file[index].visited = true;
                }
                //printf("%s\n", dir->d_name);
            }
        }
        closedir(d);
    }
    setDeletedFiles();

    return 0;
}

int sendDataToServer(){

	int i;

    for (i = 0; i < folder.size; ++i)
    {
        if (folder.file[i].status == 'M' || folder.file[i].status == 'C')
        {
            // write file to server
        }
        else if (folder.file[i].status == 'D')
        {
            // send the filename or file struct
        }   
    }    
    return 0;    
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

char* readFileBytes(const char *name, long *lenf){  
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

void writeFileBytes(const char *name, char* data, long lenf){  
    FILE *fl = fopen(name, "wb");  
    
    fwrite(data, lenf, 1, fl);

    fclose(fl);

    return;  
} 