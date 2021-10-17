#!/bin/bash
echo "███████╗ ██████╗  █████╗ ██████╗ ███╗   ██╗██╗     ██╗    ██╗     ██╗ ██████╗███████╗██████╗ ███████╗
╚══███╔╝██╔════╝ ██╔══██╗██╔══██╗████╗  ██║██║     ██║    ██║     ██║██╔════╝╚══███╔╝██╔══██╗██╔════╝
  ███╔╝ ██║  ███╗███████║██║  ██║██╔██╗ ██║██║     ██║    ██║     ██║██║       ███╔╝ ██████╔╝█████╗  
 ███╔╝  ██║   ██║██╔══██║██║  ██║██║╚██╗██║██║██   ██║    ██║     ██║██║      ███╔╝  ██╔══██╗██╔══╝  
███████╗╚██████╔╝██║  ██║██████╔╝██║ ╚████║██║╚█████╔╝    ███████╗██║╚██████╗███████╗██████╔╝███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚════╝     ╚══════╝╚═╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝"

if [ $# == 0 ]
then
	exit
fi

i=10
if [ $2 -gt $1 ]
then
	a=$(( ( RANDOM %( $2 - $1 + 1) ) + $1))
else
	echo "Max jest mniejszy bądź równy min"
	exit
fi
b=-1
echo "Podaj liczbe"
while [ $b != $a ]
do
	if [ $i == 0 ]
	then
		echo "PRRZEGRANA! - wykorzystano 10 ruchow"
		exit
	fi
	read b
	if [ "$b" -lt "$a" ]
	then
		echo "Liczba szukana jes wieksza"
	fi
	if [ "$b" -gt "$a" ]
	then
		echo "Liczba szukana jest mniejsza"
	fi
	i=$(( $i-1 ))
done
echo "GRATULACJE ZGADŁEŚ LICZBĘ"
