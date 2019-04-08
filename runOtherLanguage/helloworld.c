#include <stdio.h>

int main(){

	int a[7]={0};
	char c;
	int i;

	for(i = 0; i < 7; i++) {
		scanf("%d",&a[i]);
	}


	for(i = 0; i < 7; i++) {
		printf("Hello World! %d", a[i]);
	}
	
	

	return 0;
}