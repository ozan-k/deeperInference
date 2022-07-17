#!/usr/bin/env python3
# coding: utf-8

# https://fadoss.github.io/maude-bindings/
# https://github.com/fadoss/maude-bindings
# https://docs.python.org/3/library/itertools.html

import maude
import itertools
import time
import os
import seeds

#               1,2,3,4,5, 6, 7, 8, 9,10
seed_lengths = [1,2,3,5,7,11,15,22,30,42]

def get_atoms(s):
	flag = False
	result = []
	for i in s:
		if not i in ["{","}","[","]"," ",","]:
			if i == "-":
				flag = True
			elif flag:
				flag = False
			else:
				result.append(i)	
	return result        


def get_difference(smaller_atoms,larger_atoms):
	# print(smaller_atoms,larger_atoms)
	for a in smaller_atoms:
		if a in larger_atoms:
			larger_atoms.remove(a)
			# print("yes",a,larger_atoms)
		else:
			return "x"	
	if len(larger_atoms) == 1:
		return larger_atoms[0]
	else:
		return "x"			

def get_seeds_of(p,q):
	this_str = seeds.seeds[str(p)][q]
	larger_atoms = get_atoms(this_str)
	source_seeds = seeds.seeds[str(p-1)]
	for k,item in enumerate(source_seeds):
		smaller_atoms = get_atoms(item)
		# print(k,end=" ")
		difference = get_difference(smaller_atoms,larger_atoms.copy())
		if difference != "x":
			return p-1,k,difference
	
def seeds_of_atom_count(atom_count):		
	for i in range(seed_lengths[atom_count-1]):
		m,n,atom, = get_seeds_of(atom_count,i)
		print("build_this(" + str(m) + "," + str(n) + ",'" + atom + "'," + str(atom_count) + "," + str(i) + ")")


for i in range(7,11):
	seeds_of_atom_count(i)
	print("# ~~~~~~~~~~~")
