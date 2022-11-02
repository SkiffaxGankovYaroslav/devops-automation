#!/bin/bash
# Created by yaroslav.gankov (skiff)
#
# ----------------------------------
# Script reads file 'terraform_show' and outputs resources that match the first argument
# Example of usage with argument 'module.peer-devops-access-devops-k8s':
# ./script_terraform_show_all_resources_from_module.sh module.peer-devops-access-devops-k8s
#
# It is needed to create file terraform_show. Example:
# terraform show -no-color > terraform_show
# ----------------------------------
#
filename="terraform_show"
if [ "$2" != "" ] ; then #если параметр передан, то перезаписываем его
    filename="$2"
fi
echo -e "\033[33mResources:\033[0m"
cat ${filename} | grep --color=always "$1" | sed -e "s/^# //;s/:$/;/"
echo -e "\033[33mMore Data with id:\033[0m"
cat ${filename} | grep -A 50 --color=always -P "$1" | grep -C 100 --color=always -P "$1|\bid"
