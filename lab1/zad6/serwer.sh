#!/bin/bash

f1=0
f2=0

if [ $# == 0 ]
then
	exit
fi

rm gra.log 2&>/dev/null

sh gracz1.sh &
sh gracz2.sh &

for (( i=0; i<$1; i++ ))
do
	echo "start" > "komenda.txt"
	until [ -f 'los1.txt' ] && [ -f 'los2.txt' ]
	do
		sleep 0.01
	done
	sleep 0.1
	rm komenda.txt
	g1=`cat los1.txt`
	g2=`cat los2.txt`

	if [ $g1 = $g2 ]
	then
		echo "Remis" >> "gra.log"
	elif ([ $g1 = "papier" ] && [ $g2 = "kamien" ]) || ([ $g1 = "kamien" ] && [ $g2 = "nozyce" ]) || ([ $g1 = "nozyce" ] && [ $g2 = "papier" ])
	then
		f1=$(( $f1 + 1 ))
		echo "Gracz 1 wygrał: $g1 $g2" >> "gra.log"
	else
		f2=$(( $f2 + 1 ))
		echo "Gracz 2 wygrał: $g1 $g2" >> "gra.log"
	fi
	rm los1.txt
	rm los2.txt
done

echo "Wygrane gracza 1: $f1"
echo "Wygrane gracza 2: $f2"

echo "stop" > "komenda.txt"
sleep 1s
rm komenda.txt

