#!/bin/bash
# Created by yaroslav.gankov (skiff)
##### The first argument is filename where is resources to remove
##### The second argument (optional) is start line number to remove from file
##### Comments sets by char '#'. All the lines that starts with '#' will be be ignored
filename="to_import.txt"
if [ "$1" != "" ] ; then #если параметр передан, то перезаписываем его
    filename="$1"
fi

if [ "$2" != '' ] ; then
    start_line="$2"
else
    start_line=1
fi

echo "Filename: ${filename}"
number_of_lines=$(wc "${filename}" | awk '{ print $1 }')
echo "Number of lines: $number_of_lines"
echo -e "\033[33m-----------main loop start-----------\033[0m"
counter=1

#main loop
while read y
do
temp=$y
if [ "$counter" -ge "$start_line" ] ; then
    if [ $(echo "${temp}" | grep -v "#") ] ; then
        #First - name_resource in code. Second - id or identifier resource in real. Delimiter is char ';'
        resource_in_code=$(echo "${temp}" | cut -d \; -f 1)
        resource_in_real_id=$(echo "${temp}" | cut -d \; -f 2)
        echo -e "\033[33m${counter}/${number_of_lines}: terraform state rm ${resource_in_code}\033[0m"
        terraform state rm "${resource_in_code}"
    else
        echo -e "\033[33m${counter}/${number_of_lines}: \033[31mignored/commented: \033[37m${temp}\033[0m"
    fi
fi
((counter++))
done < "${filename}"
echo -e "\033[33m-----------main loop end-----------\033[0m"
