# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:22:03 2023

@author: pylya
"""

from Heuristics import *
import sys
import numpy as np

np.random.seed(2)
f_name = "C:\\Users\\pylya\\Desktop\\PhD\\PhD\\github\\CSPLib\\Dataset\\N2OR_New.xlsx"
for i in range(1):
    p = Problem(file_name = f_name)
    parameters = p.ReadProblemInstance()
    p.FindConflicts()
    p.AssignTimezonesPenalties(parameters)
    sol = Solution(p, parameters)
    sol = Random(p, sol)
    print(sol.getSolTracks())
    print(sol.getSolSubmissions())
    print(sol.EvaluateTracksBuildings())
    print('All submissions scheduled? ', sol.EvaluateAllSubmissionsScheduled())
    print('Is solution valid? ', sol.ValidateSolution())
    sys.exit()
    
    opt = Optimisation(p, sol)
    
    '''
    Exact methods: BasicModel, AdvancedModel, ApproximationModel, RelaxedModel
    Hyper-Heuristics: RHH, iRHH, LRHH
    Matheuristic: MH
    run_time in seconds [Only applicable to heuristics]
    '''
    
    s_time = time()
    opt.Solve(p, sol, method = 'MH', run_time = 2)
    
    print('Run time:', round((time() - s_time) / 60, 2), 'minutes')
    print(sol.getSolTracks())
    print(sol.getSolSubmissions())
    print('Objective Value:', sol.EvaluateSolution())
    print('All Submissions Scheduled?', sol.EvaluateAllSubmissionsScheduled())
    print('Is Solution Valid?', sol.ValidateSolution())
    sol.PrintViolations()
    #sol.toExcel(file_name = 'Solution.xlsx')