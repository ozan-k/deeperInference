#!/usr/bin/env python3
# coding: utf-8

import os
os.system(' ./strategy_di_maude.py di_ci.maude ../FormulaeNormal/  0 16')

os.system(' ./strategy_di_maude.py di.maude ../FormulaeNormal/  0 6')

os.system(' ./strategy_sc_maude.py sc_ci.maude ../FormulaeNormal/  0 6')

os.system(' ./strategy_sc_maude.py sc.maude ../FormulaeNormal/  0 6')
