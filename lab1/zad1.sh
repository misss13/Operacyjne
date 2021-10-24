#!/bin/bash

#echo $@
#echo $#
#echo $0

if [ $# == 0 ]
then
	exit
fi

find $1 -type f -size +$2c  -printf "%T@ %Tc %p rozmiar = %s\n" | sort -nr
