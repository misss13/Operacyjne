#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int glob_stat = 1;
int *glob_dyn;

int main(){
	FILE *plik = fopen("dootwarcia", "w");
	char a[5];
	int b;
	glob_dyn = malloc(sizeof(int));
	glob_dyn[0] = 2;
	int lok_stat = 3;
	int *lok_dyn = malloc(sizeof(int));
	lok_dyn[0] = 4;

	int pid=fork();
	if(pid < 0){
	fprintf(stderr, "Blad forkowania");
	return 1;
	}
	else if (pid == 0){
	printf("I'm child process\n my pid: %d\nmy ppid: %d\n", getpid(), getppid());
	scanf("%s", a);
	fputs("child open file\n", plik);
	fclose(plik);
	}
	else {
	wait(NULL);
	printf("I'm parent process my pid: %d\n", getpid());
	scanf("%d", &b);
	fputs("rodzic\n", plik);

	//wylistowanie zmiennych
	printf("globalna statyczna = %d\n", glob_stat);
	printf("globalna dynamiczna = %d\n", glob_dyn[0]);
	printf("lokalna statyczna = %d\n", lok_stat);
	printf("lokalna dynamiczna = %d\n", lok_dyn[0]);
	}

	fclose(plik);
	free(glob_dyn);
	free(lok_dyn);
	return 0;
}
