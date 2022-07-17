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
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def build(input_file):
	flag = False
	input_list = get_formulae_in("./",input_file)
	result = []
	for k,item in enumerate(input_list):
		if item[:6] == "R --> ":
			current = item.split(" --> ")[1]
			flag = True
		elif flag and item == "":
			pass
		elif flag and item[:3] == "   ":
			current += item.split("   ")[1]
		elif flag and (item[:8] == "Solution" or item[:8] == "No more "): 
			flag = False
			result.append(current)
	if flag:
		result.append(current)	
	return result

	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for i in range(0,1):
	print(i)
	input = "s_08_2" + str(i) + ".txt"
	formulae = build(input)
	output = "result"+input[1:-4]
	write_to_file("\n".join(formulae),output)
	
