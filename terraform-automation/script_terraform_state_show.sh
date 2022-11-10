#!/bin/bash
# Created by yaroslav.gankov (skiff)
# first argument (optional) - name of resource to show
filename_with_resources="terraform_state_list"
filename="terraform_show"
filename_new="/home/user/TEG/teg-cloud-terraform/workspaces/tf-live-networking/terraform_show_after"
# if [ "$1" != "" ] ; then #если параметр передан, то перезаписываем его
#     filename_with_resources="$1"
# fi

if [ "$1" != "" ] ; then #если параметр передан, то перезаписываем его
    resource="$1"
    echo $resource
fi



# debug
# resource="module.peer-devops-access-devops-k8s.aws_route.dst_route[1]"
# resource=$(echo $resource | sed "s/\[/\\\[/")
# resource=$(echo $resource | sed "s/\]/\\\]/")
# echo "$resource"
# echo "module.peer-devops-access-devops-k8s.aws_route.dst_route[1]" | grep --color=always -P "$resource"

counter=1
# counter_ploho=0
while read y
do
    temp=$y
    if [ "$1" == "" ] ; then
        resource=$(echo "${temp}" | cut -d ' ' -f 1)
    fi
    resource=$(echo "${resource}" | cut -d \; -f 1)
    resource=$(echo $resource | sed "s/\[/\\\[/")
    resource=$(echo $resource | sed "s/\]/\\\]/")
    #terraform state show "$resource" > "$filename"
    #cat "$filename" | grep -A 100 --color=always -P "$resource" |#| grep -C 100 --color=always -P "$resource|\bid.*|route_table_id.*|destination_cidr_block.*"
    echo -e "\033[33m${counter}========: ${resource}"
    echo -e "\033[33m----old----"
    temp1=$(cat "$filename" | grep -A 1000 --color=always -P "$resource" | grep -B 1000 -m 1 -P "^}" | grep -C 1000 --color=always -P "$resource|\bid.*|route_table_id.*|destination_cidr_block.*")
    echo -e "$temp1"
    echo -e "\033[33m----new----"
    temp2=$(cat "$filename_new" | grep -A 1000 --color=always -P "$resource" | grep -B 1000 -m 1 -P "^}" | grep -C 1000 --color=always -P "$resource|\bid.*|route_table_id.*|destination_cidr_block.*")
    #$resource(.*\n){1,}?^}
    echo -e "$temp2"
    # if [ -z "$temp1"] ; then
    #     echo "ololo equal"
    #     ((counter_ploho++))
    # fi
    echo -e "\033[33m${counter}========: ${resource}"
    #id1=$(echo "$temp2" | grep -P "\bid.*")
    #echo "$temp2" | grep -C 100 --color=always -P "\bid.*|route_table_id.*|destination_cidr_block.*"
    #echo "$id1"
    #cat "$filename" | grep --color=always -oP "$resource.*" #| grep -C 100 --color=always -P "$resource|\bid.*|route_table_id.*|destination_cidr_block.*"
    #echo "-----------"
    #cat "$filename" | sed -rE "s/(.*\n){1,}.*$resource/ss/" | head -n 30
    if [ "$1" != "" ] ; then
        exit
    fi
    ((counter++))
done < "${filename_with_resources}"
# echo "counter_ploho: $counter_ploho"