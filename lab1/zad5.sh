#!/bin/bash

#echo "$# liczba argumentow, $@ tablica argumentów, $? jak ma sie ostatnia komenda"
#iPad=123 $ i=foo $ echo "${!i*}" i iPad# indirect expansion

if [ $# == 0 ]
then
	exit
fi

for (( i=$#; i>=1; i-- ))
do
	echo -n "${!i} "
done
echo
