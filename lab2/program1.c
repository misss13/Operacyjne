#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(){
	
	char strink[10];
	FILE *pliczek;
	pliczek=fopen("/home/balalaika/Operacyjne/lab1/l1/a","r+");
	int statyczne; //statyczne
	int *dynamiczna = (int *) malloc(2*2*sizeof(int));

	int pid=fork();
	if(pid < 0){
	fprintf(stderr, "Fork Failed");
	return 1;
	}
	else if (pid == 0){
	printf("I am child process my ID is   =  %d\n" , getpid());
	//execlp("/bin/bash", "/bin/bash", "-c", "read", "a");
	int dziecko;
	scanf("%d",&dziecko);
	}
	else {
	wait(NULL);
	printf("Child Complete");
	printf("I am parent process my ID is   =  %d\n" , getpid());
	scanf("%s", strink);
	//printf("%s\n", strink);
	}

//	printf("%d/n", a);
//	int i=5;
//	while (i-- > 0){
//	printf("yooo\n");
//	}
	free(dynamiczna);
	return 0;
}
