#!/usr/bin/env python3
# coding: utf-8

# https://fadoss.github.io/maude-bindings/
# https://github.com/fadoss/maude-bindings
# https://docs.python.org/3/library/itertools.html

import maude
import itertools
import time
import os
import sys

dimension = 6
this_partition = int(sys.argv[1])
start = 17 

def decide(last,current):
	if (last == "}" and current == "[") or (last == "]" and current == "{"):
		return False
	else:
		return True	 

def pretty(s):
	new = ""
	last =""
	for current in s:
		if current != last and current != " " and decide(last,current):
			new = new + current		
		if current  == "{" or current == "[" or current  == "}" or current == "]":
			last = current
	return new.replace("{","(").replace("}",")")

def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
lst_seed_count = [1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    return item_list

def get_formulae_in(folder_path,filename):
	file1 = open(folder_path + "/" + filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

maude.init(advise=False)

maude.load('./s.maude')
nvmach = maude.getModule('S')
# nvmach_initial1 = nvmach.parseTerm('{{[a,- a],[b,- b]},[c,- c]}')
# nvmach_initial1 = nvmach.parseTerm('{{[a,- a],[b,- b]},{[c,- c],[d,- d]}}')
#nvmach_initial1 = nvmach.parseTerm('{{{{[a,- a],[b,- b]},[c, - c] },[d, - d] }, [e, - e] }')

def get_formulae_for(formula,add):
	start_time = time.time()
	this_str = "{"+ formula +" , [ "+add + " , - " + add + " ] }"
	print("Seed:",this_str)
	nvmach_initial1 = nvmach.parseTerm(this_str)
	nvmach_target1  = nvmach.parseTerm('R:Structure')
	print(nvmach_initial1, '=>!',nvmach_target1)
	lst = [ t[0] for t in nvmach_initial1.search(maude.NORMAL_FORM, nvmach_target1) ]
	result = []
	for t in lst:
		s = str(t)
		result.append(str(s)) 	
	# print(result)
	# write_to_file(result,"result_"+str(m)+"_"+str(n))
	# print(result)
	print('Search completed in')
	print('--- '+str(time.time() - start_time) + 'secs. ---')
	print()
	return result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def build_this(m,n,add,out_m,out_n,partition):
	# files = get_current_items_in("../Production/")
	if m < 10:
		file = "result_0" + str(m) + "_" + str(n) + ".txt"
	else:
		file = "result_" + str(m) + "_" + str(n) + ".txt"
	formulae = get_formulae_in("./",file)        
	all = []
	length = len(formulae)
	interval = int(length / dimension)
	begin = (partition-1)*interval
	if partition == dimension:
		end = length
	else:
		end = partition * interval
	print(begin,end)
	for f in formulae[begin:end]:
		print(f)
		all = all + get_formulae_for(f,add)
	all = list(dict.fromkeys(all))
	print(len(all))
	result = "\n".join(all)
	if out_m < 10:
		write_to_file(result,"result_0"+str(out_m)+"_"+str(out_n)+"_"+str(partition))
	else:	 
		write_to_file(result,"result_"+str(out_m)+"_"+str(out_n)+"_"+str(partition))
	print("~~~~~~~~~~~~~~~~~~~~~~~")     
    

# last argument is the partition is 1 or 2 or 3 or 4

build_this(start,0,'a',start+1,0,this_partition)


