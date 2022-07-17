#!/usr/bin/env python3
# coding: utf-8

# https://fadoss.github.io/maude-bindings/
# https://github.com/fadoss/maude-bindings
# https://docs.python.org/3/library/itertools.html

import maude
import itertools
import time
import os

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

def build_this(m,n,add,out_m,out_n):
	# files = get_current_items_in("../Production/")
	if m < 10:
		file = "result_0" + str(m) + "_" + str(n) + ".txt"
	else:
		file = "result_" + str(m) + "_" + str(n) + ".txt"
	formulae = get_formulae_in("./",file)        
	all = []
	for f in formulae:
		print(f)
		all = all + get_formulae_for(f,add)
	all = list(dict.fromkeys(all))
	print(len(all))
	result = "\n".join(all)
	if out_m < 10:
		write_to_file(result,"result_0"+str(out_m)+"_"+str(out_n))
	else:	 
		write_to_file(result,"result_"+str(out_m)+"_"+str(out_n))
	print("~~~~~~~~~~~~~~~~~~~~~~~")     


# build_this(12,0,'a',13,0)
# build_this(13,0,'a',14,0)
# build_this(14,0,'a',15,0)
# build_this(15,0,'a',16,0)

build_this(16,0,'a',17,0)


# build_this(5,4,"c",6,5)
# build_this(5,4,"a",6,6)
# build_this(5,5,"d",6,7)
# build_this(5,5,"c",6,8)
# build_this(5,6,"e",6,9)
# build_this(5,6,"f",6,10)
# build_this(6,0,'a',7,0)
# build_this(6,1,'b',7,1)
# build_this(6,1,'a',7,2)
# build_this(6,2,'a',7,3)
# build_this(6,4,'c',7,4)
# build_this(6,4,'b',7,5)
# build_this(6,5,'b',7,6)
# build_this(6,5,'a',7,7)
# build_this(6,7,'d',7,8)
# build_this(6,7,'c',7,9)
# build_this(6,8,'b',7,10)
# build_this(6,9,'e',7,11)
# build_this(6,9,'d',7,12)
# build_this(6,10,'f',7,13)
# build_this(6,10,'g',7,14)
# # ~~~~~~~~~~~
# build_this(7,0,'a',8,0)
# build_this(7,1,'b',8,1)
# build_this(7,1,'a',8,2)
# build_this(7,2,'a',8,3)
# build_this(7,3,'a',8,4)
# build_this(7,4,'c',8,5)
# build_this(7,4,'b',8,6)
# build_this(7,5,'b',8,7)
# build_this(7,5,'a',8,8)
# build_this(7,6,'a',8,9)
# build_this(7,8,'d',8,10)
# build_this(7,8,'c',8,11)
# build_this(7,9,'c',8,12)
# build_this(7,9,'b',8,13)
# build_this(7,10,'a',8,14)
# build_this(7,11,'e',8,15)

# ~~~~~~~~~~~~ Done above this ~~~~~~~~~~~~~~~~~~
# build_this(7,11,'d',8,16)
# build_this(7,12,'c',8,17)
# build_this(7,13,'f',8,18)
# build_this(7,13,'e',8,19)
# build_this(7,14,'g',8,20)
# build_this(7,14,'h',8,21)
# # ~~~~~~~~~~~
# # build_this(8,0,'a',9,0)
# build_this(8,1,'b',9,1)
# build_this(8,1,'a',9,2)
# build_this(8,2,'a',9,3)
# build_this(8,3,'a',9,4)
# build_this(8,5,'c',9,5)
# build_this(8,5,'b',9,6)
# build_this(8,6,'b',9,7)
# build_this(8,6,'a',9,8)
# build_this(8,7,'b',9,9)
# build_this(8,7,'a',9,10)
# build_this(8,9,'a',9,11)
# build_this(8,10,'d',9,12)
# build_this(8,10,'c',9,13)
# build_this(8,11,'c',9,14)
# build_this(8,11,'b',9,15)
# build_this(8,12,'b',9,16)
# build_this(8,13,'a',9,17)
# build_this(8,15,'e',9,18)
# build_this(8,15,'d',9,19)
# build_this(8,16,'d',9,20)
# build_this(8,16,'c',9,21)
# build_this(8,17,'b',9,22)
# build_this(8,18,'f',9,23)
# build_this(8,18,'e',9,24)
# build_this(8,19,'d',9,25)
# build_this(8,20,'g',9,26)
# build_this(8,20,'f',9,27)
# build_this(8,21,'h',9,28)
# build_this(8,21,'i',9,29)
# # ~~~~~~~~~~~
# # build_this(9,0,'a',10,0)
# build_this(9,1,'b',10,1)
# build_this(9,1,'a',10,2)
# build_this(9,2,'a',10,3)
# build_this(9,3,'a',10,4)
# build_this(9,4,'a',10,5)
# build_this(9,5,'c',10,6)
# build_this(9,5,'b',10,7)
# build_this(9,6,'b',10,8)
# build_this(9,6,'a',10,9)
# build_this(9,7,'b',10,10)
# build_this(9,7,'a',10,11)
# build_this(9,9,'a',10,12)
# build_this(9,10,'a',10,13)
# build_this(9,12,'d',10,14)
# build_this(9,12,'c',10,15)
# build_this(9,13,'c',10,16)
# build_this(9,13,'b',10,17)
# build_this(9,14,'c',10,18)
# build_this(9,14,'b',10,19)
# build_this(9,15,'a',10,20)
# build_this(9,16,'b',10,21)
# build_this(9,16,'a',10,22)
# build_this(9,18,'e',10,23)
# build_this(9,18,'d',10,24)
# build_this(9,19,'d',10,25)
# build_this(9,19,'c',10,26)
# build_this(9,20,'c',10,27)
# build_this(9,21,'b',10,28)
# build_this(9,22,'a',10,29)
# build_this(9,23,'f',10,30)
# build_this(9,23,'e',10,31)
# build_this(9,24,'e',10,32)
# build_this(9,24,'d',10,33)
# build_this(9,25,'c',10,34)
# build_this(9,26,'g',10,35)
# build_this(9,26,'f',10,36)
# build_this(9,27,'e',10,37)
# build_this(9,28,'h',10,38)
# build_this(9,28,'g',10,39)
# build_this(9,29,'i',10,40)
# build_this(9,29,'j',10,41)
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# build_this(15,0,'a',16,0)
# build_this(16,0,'a',17,0)
# build_this(17,0,'a',18,0)
# build_this(18,0,'a',19,0)
# build_this(19,0,'a',20,0)
# build_this(20,0,'a',21,0)
# build_this(21,0,'a',22,0)
# build_this(22,0,'a',23,0)
# build_this(23,0,'a',24,0)
# build_this(24,0,'a',25,0)
# build_this(25,0,'a',26,0)
# build_this(26,0,'a',27,0)
# build_this(27,0,'a',28,0)
# build_this(28,0,'a',29,0)
# build_this(29,0,'a',30,0)