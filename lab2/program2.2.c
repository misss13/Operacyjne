#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

void obsluga_sygnalu (int sig){
	printf ("\nzłapałem sygnal %d\n", sig);
	if(sig == 2)
 		exit(0);
}
void sygnaly_ne(int sig){
	printf("");
}

int main (){
	int i;
	for ( i=1; i<=64; i++ ){
	if(signal(i, sygnaly_ne) == SIG_ERR)
		printf("SIG %d nie może być złapany\n", i);
	}
	printf("-----------------\ncała reszta może być złapana\n");
	for ( i=1; i<=64; i++ ) 
		signal(i, obsluga_sygnalu);
	while (1) {
		printf ("sobie działam\n");
		sleep (1);
	}
	return 0;
}
