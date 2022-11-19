#!/usr/bin/python
import os
import re #regular expressions
import sys

filename_for_read="terraform_show13" #из какого файла будем считывать инфу

find_start_phraze="module.sn_peering_nonprod.aws_vpc_peering_connection.connection"
find_start_bracket="{"
find_end_bracket="}"

if find_end_bracket == "}":
    find_start_bracket="{"

# if re.search("peerin1g",find_start_phraze):
#     print("naideno")
#match = re.search("connection\[0\]",find_start_phraze)
#print(match if match else 'Not found')
#exit()
try:
    f = open(filename_for_read, 'r')
except IOError as e:
    print(u'не удалось открыть файл: ',filename_for_read)
else:
    naideno=0
    naideno_global=0
    naideno_skobok=0
    counter_line=1
    # f_out = open('output_delete', 'w')
    print("Trying to find: ",find_start_phraze,". File: ",filename_for_read,sep="")
    for line in f:
        #if line.find(find_start_phraze) >= 0:
        if naideno <= 0: #чтобы не нагружать regexp, ищем лишь, когда индикатор найденной фразы меньше нуля
            if re.search(find_start_phraze,line):
                naideno+=1
                naideno_global+=1
                naideno_skobok=0
        if naideno > 0:
            if line.find(find_start_bracket) >= 0:
                naideno_skobok+=1
            else:
                if line.find(find_end_bracket) >= 0:
                    naideno_skobok-=1
                    if naideno_skobok <= 0:
                        naideno=0
            #print(naideno,":",naideno_skobok,":",line.find(find_end_bracket),"=",counter_line,": ",line,sep="",end="")
            print(line,sep="",end="")
        counter_line=counter_line+1
        #f_out.write(line)
    f.close()
    print("Find count:",naideno_global)
    # f_out.close()
#f = open(filename_for_read, 'r')
