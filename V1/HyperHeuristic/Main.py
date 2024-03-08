# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:22:03 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Optimisation import *
import sys
import numpy as np

f_name = "..\\Dataset\\N2OR.xlsx"
for i in range(1):
    p = Problem(file_name = f_name)
    parameters = p.ReadProblemInstance()
    p.FindConflicts()
    p.AssignTimezonesPenalties(parameters)
    
    sol = Solution(p)
    #sol = RandomInd(p)
    
    solver = Matheuristic(p, sol)
    s_time = time()
    solver.solve(start_time = s_time, run_time = 1)
    #solver.solve()
    
    print(sol.getSolTracks())
    print(sol.getSolSubmissions())
    print('Objective Value:', sol.EvaluateSolution())
    sol.printViolations()
    print('All submissions scheduled? ', sol.EvaluateAllSubmissionsScheduled())
    print('Is solution valid? ', sol.ValidateSolution())
    #sol.toExcel()