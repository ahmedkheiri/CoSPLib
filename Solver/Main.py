# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Optimisation import *
import sys
import numpy as np

instance = 'GECCO19'
f_name = '..\\Dataset\\'+str(instance)+'.xlsx'

p = Problem(file_name = f_name)
parameters = p.ReadProblemInstance()
p.FindConflicts()
p.AssignTimezonesPenalties(parameters)
sol = Solution(p)
    
solver = ExtendedModel(p, sol) #Available models: ExactModel(), ExtendedModel()
solver.solve(timelimit = 3600)
    
print(sol.getSolTracks())
print(sol.getSolSubmissions())
print('Objective Value:', sol.EvaluateSolution())
sol.printViolations()
print('All submissions scheduled? ', sol.EvaluateAllSubmissionsScheduled())
print('Is solution valid? ', sol.ValidateSolution())
#sol.toExcel(file_name = 'Solution'+str(instance)+'.xlsx')