#!/bin/bash

echo "metoda matematyczna $(( $1 ** $2 ))"
a=$1

for ((i = 1; i < $2; i++ ))
do
	a=$(( $a*$1	))
done
echo "metoda pentlowa $a"
