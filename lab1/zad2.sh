#!/bin/bash

echo "███████╗ ██████╗  █████╗ ██████╗ ███╗   ██╗██╗     ██╗    ██╗     ██╗ ██████╗███████╗██████╗ ███████╗
╚══███╔╝██╔════╝ ██╔══██╗██╔══██╗████╗  ██║██║     ██║    ██║     ██║██╔════╝╚══███╔╝██╔══██╗██╔════╝
  ███╔╝ ██║  ███╗███████║██║  ██║██╔██╗ ██║██║     ██║    ██║     ██║██║       ███╔╝ ██████╔╝█████╗  
 ███╔╝  ██║   ██║██╔══██║██║  ██║██║╚██╗██║██║██   ██║    ██║     ██║██║      ███╔╝  ██╔══██╗██╔══╝  
███████╗╚██████╔╝██║  ██║██████╔╝██║ ╚████║██║╚█████╔╝    ███████╗██║╚██████╗███████╗██████╔╝███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚════╝     ╚══════╝╚═╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝"
a=$(($1 + $RANDOM % ($2-$1+1))) #od 5 do 10 lub 1 do 10 lub od 0 do 10
echo "podaj liczbe"
read b
while [ "$a" != "$b" ]
do
	if [ "$a" -gt "$b" ]
	then
		echo "Liczba szukana jest większa niż $b"
	fi

	if [ "$a" -le "$b" ]
	then
		echo "Liczba szukana jest mniejsza niż $b"
	fi
	echo "podaj liczbe"
	read b
done
echo "Gratulacje zgadłeś liczbę!!!"
