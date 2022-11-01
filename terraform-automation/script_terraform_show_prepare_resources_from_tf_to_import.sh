#!/bin/bash
# Created by yaroslav.gankov (skiff)
#
#
filename="vpc-legacy-resources.tf"
if [ "$1" != "" ] ; then #если параметр передан, то перезаписываем его
    filename="$1"
fi
echo -e "\033[33mResources:\033[0m"
line1=$(cat ${filename} | egrep -v "^( ){0,}#" | grep "resource")
#echo $line1
#echo $(echo "$line1" | cut -d \" -f 2,4).$(echo "$line1" | cut -d \" -f 4)
echo "$line1" | cut -d \" -f 2,4 --output-delimiter='.' | sed 's/$/;/'
#echo -e "\033[33mMore Data with id:\033[0m"
#cat ${filename} | grep -A 50 --color=always -P "$1" | grep -C 100 --color=always -P "$1|\bid"
