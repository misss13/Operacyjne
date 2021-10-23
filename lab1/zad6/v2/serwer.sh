#!/bin/bash

if [ $# == 0 ]
then
	echo "./serwer.sh [l_gier] [l_graczy]"
	exit
fi

rm gra.log 2&>/dev/null

for (( i=1; i<=$2; i++))
do
	f[i]=0
	sh gracz.sh $i &
done

for (( i=0; i<$1; i++ ))
do
	echo "start" > "komenda.txt"
	for (( j=1; j<=$2; j++))
	do
		if [ ! -f 'los$j.txt ' ]
		then	
			sleep 0.01
		fi
	done

	sleep 0.1
	rm komenda.txt
	
	for (( j=1; j<=$2; j++))
	do
		g[j]=`cat los$j.txt`
	done
	
	for (( j=1; j<=$2; j++))
	do
		for (( k=1; k<=$2; k++))
		do
			if [ $j != $k ]
			then
				if [ ${g[j]} == ${g[k]} ] 
				then
					echo "Remis" >> "gra.log"
				elif ([ ${g[j]} = "papier" ] && [ ${g[k]} = "kamien" ]) || ([ ${g[j]} = "kamien" ] && [ ${g[k]} = "nozyce" ]) || ([ ${g[j]} = "nozyce" ] && [ ${g[k]} = "papier" ])
				then
					f[j]=$(( f[j]+1 ))
					echo "Gracz $j wygrał: ${g[j]} ${g[k]}" >> "gra.log"
				else
					echo "Gracz $j przegrał: ${g[j]} ${g[k]}" >> "gra.log"
				fi
			fi
		done
	done

	for ((j=1; j<=$2; j++ ))
	do
		rm los$j.txt
	done

done

for ((i=1; i<=$2; i++ ))
do
	echo "Wygrane gracza $i: ${f[i]}"
done

echo "stop" > "komenda.txt"
sleep 1s
rm komenda.txt

