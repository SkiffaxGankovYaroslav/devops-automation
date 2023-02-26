#!/bin/bash
if [[ "$1" == *"-"* ]] ; then
    echo "$1" | sed "s/-/_/g"
fi
if [[ "$1" == *" "* ]] ; then
    echo "$1" | sed "s/ /_/g"
fi
if [[ "$1" == *"_"* ]] ; then
    echo "$1" | sed "s/_/-/g"
fi
if [[ $(echo "$1" | grep "[-_]") ]]; then
    echo "$1" | sed "s/[-_]/./g"
fi
echo "---"
echo "$1" | cut -d \" -f 2,4 --output-delimiter='.' | sed 's/$/;/' | sed "s/ /./g"
#echo "$1" | sed "s/ /./g"
