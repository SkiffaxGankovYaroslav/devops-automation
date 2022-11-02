#!/bin/bash
# Created by yaroslav.gankov (skiff)
#for debug
filename="to_import.txt"
if [ "$1" != "" ] ; then #если параметр передан, то перезаписываем его
    filename="$1"
fi
echo "Filename: ${filename}"
echo "Number of lines: $(wc "${filename}" | awk '{ print $2 }')"
echo -e "\033[33m-----------main loop start-----------"
counter=1

#main loop
while read y
do
temp=$y
if [ $(echo "${temp}" | grep -v "#") ] ; then
    #First - name_resource in code. Second - id or identifier resource in real. Delimiter is char ';'
    resource_in_code=$(echo "${temp}" | cut -d \; -f 1)
    resource_in_real_id=$(echo "${temp}" | cut -d \; -f 2)
    echo -e "\033[33m${counter}: terraform state rm ${resource_in_code}"
    terraform state rm "${resource_in_code}"
else
    echo -e "\033[33m${counter}: \033[31mignored/commented: \033[37m${temp}"
fi
((counter++))
done < "${filename}"
echo -e "\033[33m-----------main loop end-----------"
