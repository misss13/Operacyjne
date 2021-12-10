#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <unistd>

typedef struct node {
    int val;
    struct node * next;
} node_t;

int main(int argc, char *argv[]){
	head = (node_t *) malloc(sizeof(node_t));
	int max = atoi(argv[1]);
	node_t *current, *next;
	head->number = 0;
	current = head;
	int i =1
	while(max > 0){
		sleep(1);
		i++;
		max = max - sizeof(node_t);
		next = malloc(sizeof(node_t));
		next->number = current->number+1;
		current
	}

	if (head == NULL) {
   	 return 1;
	}

	head->val = 1;
	head->next = NULL;

}
