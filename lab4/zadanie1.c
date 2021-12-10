#include <stdio.h>
#include <stdlib.h>


void statyczna(){
  double tablica[1000000];
  int b;
	scanf("%d", &b);
}


void dynamiczna(){
  int *zmienna_dynamiczna;
  zmienna_dynamiczna = (int *)malloc( 1000000 * sizeof(int));
  for(int i = 0; i<1000000; i++)
  	zmienna_dynamiczna[i]=i;
  printf("zmienna dynamiczna: %d", zmienna_dynamiczna[1]);
  free(zmienna_dynamiczna);
  //double *tablica = new double[100000000];
  int b;
  	scanf("%d", &b);
}


int main(void){
  int b;
  statyczna();
  scanf("%d", &b);
  dynamiczna();
}
