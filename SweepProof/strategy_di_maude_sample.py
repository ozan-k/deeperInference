#!/usr/bin/env python3
# coding: utf-8

import maude
import time
import os
import sys
import numpy as np
import random

try:
	maude_file = sys.argv[1]
	folder_path = sys.argv[2]
	lower_file_index = int(sys.argv[3])
	upper_file_index = int(sys.argv[4])
except:
	maude_file = "dummy.maude"
	folder_path = sys.argv[2]
	lower_file_index = 0
	upper_file_index = 0

try:
	breadthfirst = sys.argv[5] == "breadth"
except:
	breadthfirst = False

try:
	shallow = sys.argv[6] == "shallow"
except:
	shallow = False 

lengths = []
sizes = []
steps = []

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    return item_list

maude.init(advise=False)
maude.load('./'+maude_file)
s_search = maude.getModule('S_search')

def print_solution(*args):
	print(('              state = {}\n'
	       '  acc. substitution = {}\n'
	       '           function = {}\n'
		   '    variant unifier = {}').format(*args))
	
def get_path(*args):
	return str(args[2]())

def build_normal(n):
	lst = ['A','B','C','D','E','F','G','H','I','J']
	result = ""
	for i in range(n-1):
		result = result + "{ [" + lst[i] + ",- " +lst[i] + "], "
	result = result + " [" + lst[n-1] + ",- " +lst[n-1] + "] "
	for i in range(n-1):
		result = result + '} '	
	return result	 

def difference(c,s,label):
	def get_diverge_index(s1,s2):
		for k,i in enumerate(s1):
			if i != s2[k]:
				return k
		return 0
	def label_score(label):
		if label == "rule-1":
			return 1000000000
		elif label == "rule-bot":
			return 100000000
		elif label == "ai":
			return 10000000
		elif label == "switch-3c":
			return 1000000
		elif label == "switch-3d":
			return 100000
		elif label == "switch-4c":
			return 10000
		elif label == "switch-4d":
			return 1000
		else:
			return 0			
	a = get_diverge_index(c,s)
	b = get_diverge_index(c[::-1],s[::-1])
	return len(s[a:-1*b]) + label_score(label)

def one_step(formula):
	target1 = s_search.parseTerm('R')
	results = []
	pretty_c = pretty(str(formula))
	for solution in formula.search(maude.ONE_STEP,target1):
		pretty_p = pretty(str(solution[2]()[2]))
		label = str(solution[2]()[1]).split("[label ")[1].split("]")[0]
		results.append((difference(pretty_c,pretty_p,label),solution[2]()[2]))
	if shallow:
		results.sort(key=lambda x:x[0])
	else:
		results.sort(reverse=True, key=lambda x:x[0])
	return [ r[1] for r in results ]

def get_formulae_in(folder_path,filename):
	file1 = open(folder_path + "/" + filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines


def prove(stack,printProof):
	# The search space is stored in a stack.
	# Take the formula on top of the stack.  
	formula = stack[0][-1]
	k = 0
	while len(str(formula)) > 7:
		# Apply all the rule instances to the formula and collect the results in a list. 
		# Each result is a derivation.
		results = [ stack[0] + [f] for f in one_step(formula) ]    
		if results == []:
			stack = stack[1:]
		else:
			if breadthfirst:
				# Breadth-first search
				stack = stack[1:] + results 
			else:	
				# Depth-first search
				stack = [results[0]] + stack[1:] + results[1:]
		formula = stack[0][-1]
		# Stop after 100000 iterations.
		if k == 500000:
			return False
		if k % 10000 == 0:
			print(".",end="")	 	
		k+=1
	# ~~~~~~~~~~~~~~~~~~~~~~~
	print() 
	proof = stack[0]
	lengths.append(len(proof))
	size = 0
	for f in proof:
		size+=str(f).count("-") * 2  
	sizes.append(size)
	steps.append(k)
	
	print("Steps:")
	print(steps)
	print("Sizes:")
	print(sizes)

	if printProof:
		for p in proof[::-1]:
			print(p)
	return True		
			
def prove_main(formula,printProof):
	start_time = time.time()
	initial1 = s_search.parseTerm(formula)
	print(initial1)
	success = prove([[initial1]],printProof)
	#time_s = '\n\nSearch completed in\n'
	time_s = '--- '+str(time.time() - start_time) + 'secs. ---\n'
	print(time_s)
	return success

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def prove_all(folder,number,printProof):
	lst = []
	current_list = get_current_items_in(folder+"/")
	# print(current_list)
	file = current_list[number]
	# reading the file content and assign each line to a list element
	formulae = get_formulae_in(folder,file)
	length = str(len(formulae)) 
	print()
	print(length,"formulas in",file)
	print()
	start_time = time.time()
	result = {}
	f_lst = random.sample(range(len(formulae)),100)
	print(f_lst)
	for k in f_lst:
		f = formulae[k]
		print(k,"/",length)
		if not prove_main(f,printProof):
			lst.append(k)
			# break
	time_s = '\n\nSearch completed in\n'
	duration = time.time() - start_time
	time_s = time_s + '--- '+str(duration) + 'secs. ---\n'
	print(time_s)
	print(lst)
	result["mean length"] = np.mean(lengths)
	result["sd length"] = np.std(lengths)
	result["mean size"] = np.mean(sizes)
	result["sd size"] = np.std(sizes)
	result["mean steps"] = np.mean(steps)
	result["sd steps"] = np.std(steps)
	result["length"] = length
	result["failed"] = lst
	result["duration"] = duration
	return file,result,duration 

def enumerate_files():
	current_list = get_current_items_in(folder_path)
	for k,f in enumerate(current_list):
		print(k,f)

if lower_file_index == 0 or upper_file_index  == 0:
	print()
	enumerate_files()
	print()
	print("Specify the begin and end index of the files given, for example, among those above to prove.")
	print()
	print("Example: the following command will prove all the formulae in the files with index 1,2, and 3.")
	print("./strategy_di_maude.py di_ci.maude ../FormulaeNormal/ 1 4")
	print("Example: the following command will prove all the formulae in the files with index 1,2, and 3.")
	print("./strategy_di_maude.py di_ci.maude ../FormulaeNormal/ 1 4 depthfirst shallow")
	print()
else:	
	result = {}
	for i in range(lower_file_index,upper_file_index):
		lengths = []
		sizes = []
		steps = []	
		name,this,duration = prove_all(folder_path,i,True)
		result[name] = this
	print(result)
	f_type =  "_" + "_".join(folder_path.split("/")[1:])
	if breadthfirst:
		f_type = f_type + "_breadthfirst"
	if shallow:
		f_type = f_type  + "_shallow"
	write_to_file(str(result),maude_file + f_type + str(lower_file_index) + "_" + str(upper_file_index))


# 0 result_01_0.txt
# 1 result_02_0.txt
# 2 result_03_0.txt
# 3 result_04_0.txt
# 4 result_05_0.txt
# 5 result_06_0.txt
# 6 result_07_0.txt
# 7 result_08_0.txt
# 8 result_09_0.txt
# 9 result_10_0.txt
# 10 result_11_0.txt
# 11 result_12_0.txt
# 12 result_13_0.txt
# 13 result_14_0.txt
# 14 result_15_0.txt
