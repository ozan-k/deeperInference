#!/usr/bin/env python3
# coding: utf-8

# https://fadoss.github.io/maude-bindings/
# https://github.com/fadoss/maude-bindings
# https://docs.python.org/3/library/itertools.html

import maude
import itertools
import time
import seeds

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

maude.init(advise=False)

maude.load('./s.maude')
nvmach = maude.getModule('S')
# nvmach_initial1 = nvmach.parseTerm('{{[a,- a],[b,- b]},[c,- c]}')
# nvmach_initial1 = nvmach.parseTerm('{{[a,- a],[b,- b]},{[c,- c],[d,- d]}}')
#nvmach_initial1 = nvmach.parseTerm('{{{{[a,- a],[b,- b]},[c, - c] },[d, - d] }, [e, - e] }')

def get_formulae_for(m,n):
	start_time = time.time()
	this_str = seeds.seeds[str(m)][n]
	print("Seed:",this_str)
	nvmach_initial1 = nvmach.parseTerm(this_str)
	nvmach_target1  = nvmach.parseTerm('R:Structure')

	print(nvmach_initial1, '=>!',nvmach_target1)
	lst = [ t[0] for t in nvmach_initial1.search(maude.NORMAL_FORM, nvmach_target1) ]
	result = ""
	for t in lst:
		s = str(t)
		result = result + str(s) + "\n" 	
	write_to_file(result,"result_"+str(m)+"_"+str(n))
	# print(result)
	print('Search completed in')
	print('--- '+str(time.time() - start_time) + 'secs. ---')
	print()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# for i in range(2,8):
# get_formulae_for(6,2)

for i in range(5,11):
	print(i)
	get_formulae_for(6,i)
# [a,[b,[{c,c},[{- c,- c},[{- c,- c},[{c,- a},{c,- b}]]]]]] 3848 (6,4)
# [a,[a,[{a,a},[{a,a},[{- a,- a},[{- a,- a},[{- a,- a},{a,- a}]]]]]]] 284 (7,0)
			
        




