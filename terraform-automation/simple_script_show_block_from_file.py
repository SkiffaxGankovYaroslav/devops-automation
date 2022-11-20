#!/usr/bin/python3
#import os
import re #regular expressions
#import sys #для передачи параметров
import argparse #для передачи параметров

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_to_read', nargs='?') # название первого параметра
    parser.add_argument('string_to_find', nargs='?')
    parser.add_argument('skobka', nargs='?')
    parser.add_argument('write_to_file', nargs='?')
    return parser

filename_for_read="terraform_show13" #из какого файла будем считывать инфу

find_start_phraze="module.sn_peering_nonprod.aws_vpc_peering_connection.connection"
find_start_bracket="{"
find_end_bracket="}"
write_to_file="" #если не пусто, то записываем в файл

#переопределяем переменные, если были получены аргументы
parser_arguments = createParser()
arguments = parser_arguments.parse_args()
if arguments.file_to_read:
    filename_for_read=arguments.file_to_read
if arguments.string_to_find:
    find_start_phraze=arguments.string_to_find
if arguments.skobka:
    find_end_bracket=arguments.skobka
if arguments.write_to_file:
    write_to_file=arguments.write_to_file
#заменяем скобки,чтобы читались regexp корректно
find_start_phraze=find_start_phraze.replace("[","\[")
find_start_phraze=find_start_phraze.replace("]","\]")
#указываем соответствующую открывающую скобку
if find_end_bracket == "}":
    find_start_bracket="{"

output_var="" #в эту переменную будет заноситься всё найденное
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
    print("Phraze: ",find_start_phraze,". File: ",filename_for_read,sep="")
    print("-----")
    for line in f:
        #if line.find(find_start_phraze) >= 0:
        if naideno <= 0: #чтобы не нагружать regexp, ищем лишь, когда индикатор найденной фразы меньше нуля
            if re.search(find_start_phraze,line):
                naideno+=1
                naideno_global+=1
                naideno_skobok=0
        if naideno > 0:
            #print(line,sep="",end="")
            output_var+=line
            if line.find(find_start_bracket) >= 0:
                naideno_skobok+=1
            else:
                if line.find(find_end_bracket) >= 0:
                    naideno_skobok-=1
                    if naideno_skobok <= 0:
                        naideno=0
                        #print("")
                        output_var+=""
            #print(naideno,":",naideno_skobok,":",line.find(find_end_bracket),"=",counter_line,": ",line,sep="",end="") #debug
        counter_line=counter_line+1
    print(output_var)
    if write_to_file != "":
        filename_to_write=open(write_to_file,'w')
        filename_to_write.write(output_var)
    f.close()
    print("-----")
    print("Phraze: ",find_start_phraze,". File: ",filename_for_read,sep="")
    print("Find total count:",naideno_global)
