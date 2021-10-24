#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int main(){
	
	int pid=fork();
	if(pid < 0){
	fprintf(stderr, "Fork Failed");
	return 1;
	}
	else if (pid == 0){
	printf("I am child process my ID is   =  %d\n" , getpid());
	execlp("/bin/ls", "ls", NULL);
	}
	else {
	wait(NULL);
	printf("Child Complete");
	 printf("I am parent process my ID is   =  %d\n" , getpid());
	}

//	int i=5;
//	while (i-- > 0){
//	printf("yooo\n");
//	}

	return 0;
}
