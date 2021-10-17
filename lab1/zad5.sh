#!/bin/bash

#echo "$#"

if [ $# == 0 ]
then
	exit
fi

for (( i=$#; i>=1; i-- ))
do
echo -n "${!i} "
done
echo
