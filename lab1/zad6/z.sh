#!/bin/bash

echo "start" > komenda.txt
sh losuj.sh
sleep(10)
a= $(( $1-1 ))
for (( i=0; i<$a; i++))
do
	sleep(5)
	if [[ -r "los1.txt" ]]
	then
		if [[ -r "los2.txt" ]]
	fi
done

