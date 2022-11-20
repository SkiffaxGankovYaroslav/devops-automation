#!/usr/bin/python3
# Скрипт ищет в файле 'filename_for_read' блоки и выводит их в консоль
# Блок имеет начало, равное 'find_start_phraze' и конец 'find_end_bracket'
# 
# Аргументы:
# 1 - source file, из которого будет производиться чтение
# 2 - find_start_phraze, строка поиска. Также можно указать название файла, тогда вместо фразы будет использоваться файл с фразами
# 3 - find_end_bracket, индикатор окончания блока.
# 4 - write_to_file, имя файла, в который будет записан все найденные блоки

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
#указываем соответствующую открывающую скобку
if find_end_bracket == "}":
    find_start_bracket="{"

# Далее пробуем открыть файл, имя которого указано в 'find_start_phraze'.
# Если файла нет, то предполагаем, что указана фраза и ищем её
try:
    find_start_phraze = open(find_start_phraze, 'r')
except IOError as e:
    print("log: using patterns from variable")
    find_start_phraze=list([find_start_phraze])
else:
    print("log: using patterns from file")

# for phraze in find_start_phraze:
#     print("=====Iteration:",phraze)
# exit()

naideno_global=0
counter_global=0
output_var="" #в эту переменную заносится всё найденное
for phraze in find_start_phraze:
    counter_global+=1
    #проверяем, есть ли комментарий
    phraze=phraze.replace("\n","")
    if re.search("^( ){0,}#",phraze):
        #print(phraze)
        print("X     ",counter_global,":IGNORED:",phraze,". Source File: ",filename_for_read,sep="")
        #print("↓-----",counter_global,":IGNORED:",phraze,". Source File: ",filename_for_read,sep="")
        #print("↑-----",counter_global,":IGNORED:",phraze,". Source File: ",filename_for_read,sep="")
        continue
    if re.search("^$",phraze):
        print("X     ",counter_global,":EMPTY_LINE: Source File: ",filename_for_read,sep="")
        continue
    phraze=re.sub(";.*","",phraze) #отсекаем правую часть,что за символом ';'
    #заменяем скобки,чтобы читались regexp корректно
    phraze=phraze.replace("[","\[")
    phraze=phraze.replace("]","\]")
    #print("===BV3..Z
    # ==Iteration:",phraze)
    try:
        f = open(filename_for_read, 'r')
    except IOError as e:
        print(u'не удалось открыть файл: ',filename_for_read)
    else:
        naideno=0
        naideno_skobok=0
        counter_line=1
        # f_out = open('output_delete', 'w')
        print("↓-----",counter_global,":",phraze,". Source File: ",filename_for_read,sep="")
        for line in f:
            #if line.find(phraze) >= 0:
            if naideno <= 0: #чтобы не нагружать regexp, ищем лишь, когда индикатор найденной фразы меньше нуля
                if re.search(phraze,line):
                    naideno+=1
                    naideno_global+=1
                    naideno_skobok=0
            if naideno > 0:
                print(counter_line,": ",line,sep="",end="")
                output_var+=line
                if line.find(find_start_bracket) >= 0:
                    naideno_skobok+=1
                else:
                    if line.find(find_end_bracket) >= 0:
                        naideno_skobok-=1
                        if naideno_skobok <= 0:
                            naideno=0
                            #print("")
                            output_var+="\n"
                #print(naideno,":",naideno_skobok,":",line.find(find_end_bracket),"=",counter_line,": ",line,sep="",end="") #debug
            counter_line=counter_line+1
        print("↑-----",counter_global,":",phraze,". Source File: ",filename_for_read,sep="")
        f.close()
#print(output_var)
if write_to_file != "":
    filename_to_write=open(write_to_file,'w')
    filename_to_write.write(output_var)
    filename_to_write.close()
        
        
print("====")
print("Find total count:",naideno_global)
print("====log: end of script===")
