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


def copar_join(lst):
	result = ""
	length = len(lst) - 1
	for k,i in enumerate(lst):
		if k < length:
			result += "{ " + i + ", "	
		else:
			result += i
	for i in range(length):
		result += " }"
	return result 

def generate(n):
	lst = ["[ a , - a ]"] * n
	return copar_join(lst)

def get_seeds(n):
	result = []
	for i in range(2,n):
		result.append(generate(i))
	return result

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

def any_steps(formula):
	target1 = nvmach.parseTerm('R')
	results = []
	# maude.ONE_STEP
	for solution in formula.search(maude.ANY_STEPS,target1):
		results.append(solution[0])
		# results.append(solution[2]()[1])
	return results

def count_string(c):
	if c < 10:
		return "000"+str(c)
	elif c < 100:
		return "00"+str(c)
	elif c < 1000:
		return "0"+str(c)
	elif c < 10000:
		return ""+str(c)
	else:
		return str(c)				

def get_all(seeds,filename):
	lst = [ nvmach.parseTerm("{ [ a , - a ] , " + seed + "}") for seed in seeds ]
	result = [] 
	length = str(len(lst))
	count = 0
	for k,item in enumerate(lst):
		start_time = time.time()
		result += any_steps(item)
		print(str(k) +"/" + length)
		time_s = 'search completed in\n'
		duration = time.time() - start_time
		time_s = time_s + '--- '+str(duration) + 'secs. ---\n'
		print(time_s)
		if (k+1) % 100 == 0:
			count += 1
			print(count)	
			result = list(dict.fromkeys(result))
			print(len(result),"formulae.")	
			output = "\n".join([str(i) for i in result])
			write_to_file(output,"Out/"+filename+"_"+count_string(count))
			result  = []
	if (k+1) % 100 != 0:
		count += 1	
		result = list(dict.fromkeys(result))
		print(len(result),"formulae.")	
		output = "\n".join([str(i) for i in result])
		write_to_file(output,"Out/"+filename+"_"+count_string(count))
			
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def build(input_file):
	input_list = get_formulae_in("./",input_file)
	get_all(input_list,input_file[:-4])
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
build("result_07.txt")

