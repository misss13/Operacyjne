#!/bin/bash
p="los$1.txt"

while :
do
	until [ -f "komenda.txt" ] && [ ! -f $p ]
	do
		sleep 0.01s
	done

	c=`cat komenda.txt`
	if [ $c = "stop" ]
	then
		exit
	fi
	if [ $c = "start" ]
	then
		ruch=$(( ($RANDOM)%3 ))
		if [ $ruch -eq 0 ]
		then
			echo "papier" > $p
		elif [ $ruch -eq 1 ]
		then
			echo "nozyce" > $p
		else
			echo "kamien" > $p
		fi
	fi
done
