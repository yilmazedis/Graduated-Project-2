#include <dirent.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>


#define SIZE 100

struct file
{
    char filename[SIZE];
    char status;
    bool visited;
    struct timespec lastModification;
};


struct file myFiles[SIZE];
int numOfFiles = 0;


void setVisitedFalse();
int isFileExist(char * filename);
void showFiles();
int checkFiles();
void setDeletedFiles();
int sendDataToServer();


int main(void){



    while(1){
        checkFiles();
        showFiles();
        sleep(2);
    }

    return 0;
}

void setVisitedFalse(){

    for (int i = 0; i < SIZE; ++i)
    {
        myFiles[i].visited = false;
    }

}

int isFileExist(char * filename){

    for (int i = 0; i < numOfFiles; ++i)
    {
        if (strcmp(myFiles[i].filename,filename) == 0)
        {
            return i;
        }
    }

    return -1;

}

void showFiles(){

    for (int i = 0; i < numOfFiles; ++i)
    {
        if (myFiles[i].status != 'D')
        {
            printf("%s %c\n",myFiles[i].filename, myFiles[i].status);
        }
    }

}

void setDeletedFiles(){
    for (int i = 0; i < numOfFiles; ++i)
    {

        if(myFiles[i].visited == false){
            myFiles[i].status = 'D';
            printf("hi\n");
        }
    }
}


int checkFiles(){
    DIR *d;

    struct dirent *dir;

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

                //printf("Last file modification:   %s", ctime(&statOfFile.st_mtime));

                int index = isFileExist(dir->d_name);
                if(index == -1){
                    strcpy(myFiles[numOfFiles].filename,dir->d_name);
                    myFiles[numOfFiles].status = 'C';
                    myFiles[numOfFiles].visited = true;
                    myFiles[numOfFiles].lastModification = statOfFile.st_mtim;
                    numOfFiles++;
                }
                else{
                    if (myFiles[index].lastModification.tv_sec != statOfFile.st_mtime)
                    {
                        myFiles[index].status = 'M';                                // Modified
                        myFiles[index].lastModification = statOfFile.st_mtim;
                    }
                    else{
                        myFiles[index].status = 'U';                                // Unchanged
                    }
                    myFiles[index].visited = true;
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

    for (int i = 0; i < numOfFiles; ++i)
    {
        if (myFiles[i].status == 'M' || myFiles[i].status == 'C')
        {
            // write file to server
        }
        else if (myFiles[i].status == 'D')
        {
            // send the filename or file struct
        }
        
    }
    
    return 0;    
}