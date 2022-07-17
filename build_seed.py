#!/usr/bin/env python3
# coding: utf-8

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

seeds = [""]
for i in range(1,21):
    this_seed = generate(i)
    seeds.append(this_seed)

import json

with open('seeds.json', 'w', encoding ='utf8') as json_file:
    json.dump(seeds, json_file)	


# def write_to_file(content,filename):
#     f = open(filename+'.txt', "w")
#     f.write(content)
#     f.close()


# write_to_file("\n".join(seeds),"seeds")
# print("\n".join(result),"seeds")
