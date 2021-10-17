#!/bin/bash

if [ $# == 0 ]
then
	exit
fi

find $1 -type f -size +$2c
