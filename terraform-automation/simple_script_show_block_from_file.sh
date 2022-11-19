#!/bin/bash
# поиск в файле блока, который начинается с указанной фразы и заканчивается символом
# 1 аргумент - файл для чтения
# 2 аргумент - искомая фраза
# 3 аргумент - обозначение конца блока (обычно и по умолчанию это символ '}')
# 4 аргумент - если не указано "true", то фраза считывается как есть (без regexp). "true" - и искомая фраза будет восприниматься как regexp
#
filename_for_read="terraform_show13" #из какого файла будем считывать инфу

find_start_phraze="module.sn_peering_nonprod.aws_vpc_peering_connection.connection"
find_end_phraze="}"

if [ "$1" != "" ] ; then
    filename_for_read="$1"
fi

if [ "$2" != "" ] ; then
    find_start_phraze="$2"
fi

if [ "$3" != "" ] ; then
    find_end_phraze="$3"
fi

if [ "$find_end_phraze" = "}" ] ; then
    find_open_bracket="{"
else
    if [ "$find_end_phraze" = ")" ] ; then
        find_open_bracket="("
    fi
fi

if [ "$4" == "true" ] ; then
    regexp_true="$4"
    find_start_phraze=$(echo $find_start_phraze | sed "s/\[/\\\[/")
    find_start_phraze=$(echo $find_start_phraze | sed "s/\]/\\\]/")
fi

# echo "find_open_bracket: $find_open_bracket"
# echo "find_start_phraze: $find_start_phraze"

naideno=0
naideno_skobok=0
counter=1
if [ -f  "$filename_for_read" ] ; then
    while read y
    do
        temp=$y
        
        # if [[ "$temp" == *"$find_start_phraze"* ]] ; then
        #     ((naideno++))
        # fi
        #if [ -z "$regexp_true" ]; then            echo "if" ; else echo "else" ; fi
        #         #grep -q "$find_start_phraze"
        # else
        #     echo "else"
        #     #grep -q -F "$find_start_phraze"
        # fi;

        if [ -z "$regexp_true" ]; then 
            if echo "$temp" | grep -q -F "$find_start_phraze" ; then
                naideno=1
                naideno_skobok=0
            fi
        else
            if echo "$temp" | grep -q "$find_start_phraze" ; then
                naideno=1
                naideno_skobok=0
            fi
        fi
        # echo "$counter: $naideno. $temp"
        if (( "$naideno" > 0 )) ; then
            if echo "$temp" | grep -q -F "$find_open_bracket" ; then
                ((naideno_skobok++))
            fi
            echo "$temp"
            if echo "$temp" | grep -q -F "$find_end_phraze" ; then
                ((naideno_skobok--))
                if (( "$naideno_skobok" <= 0 )) ; then
                naideno=0
                fi
            fi
            
        fi
        #echo "$counter: $naideno"
        ((counter++))
    done < "${filename_for_read}"
else
    echo "Файл не найден: '$filename_for_read'"
fi
