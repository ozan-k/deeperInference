#!/usr/bin/env python3
# coding: utf-8

import maude
import time
import os

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


def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()

def generate(n):
	lst = ["[ a , - a ]"] * n
	return copar_join(lst)

result = []
for i in range(2,101):
    result.append(generate(i))
write_to_file("\n".join(result),"seeds")

