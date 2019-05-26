#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void fillArray(int array[1000],int *size){char str[10];FILE *fptr;int len;fptr=fopen("outputs","r");while(fgets(str,sizeof(str),fptr)){len=strlen(str);if(str[len-1]=='\n')str[len-1]=0;array[*size]=atoi(str);(*size)++;}fclose(fptr);}
void emptyArray(int array[1000],int size){FILE *fptr;int i;fptr=fopen("outputs","w");for(i=0;i<size;++i){fprintf(fptr,"%d\n",array[i]);}fclose(fptr);}

int main(){

    int size, i;
    int array[1000];

    fillArray(array,&size);

    for (i = 0; i < size; ++i)
        array[i] += 1;
    
	emptyArray(array,size);

	return 0;
}