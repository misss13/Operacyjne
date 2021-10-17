#!/bin/bash

if [ $# == 0 ]
then
	exit
fi

convert -quiet -density 600 $1 -resize 25% pom.png
composite -quiet -gravity center -geometry +$3-$4 $2 pom.png result.png
convert -quiet result.png dokument1.pdf
