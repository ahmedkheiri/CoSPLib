# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Solution import *

p = Problem(file_name = "..\\Dataset\\N2OR.xlsx")
parameters = p.ReadProblemInstance()
p.FindConflicts()
p.AssignTimezonesPenalties(parameters)
sol = Solution(p)
sol.ReadSolution(file_name = "..\\Solutions\\SolutionN2OR.xlsx")

print(sol.getSolTracks())
print(sol.getSolSubmissions())
print('Objective Value:', sol.EvaluateSolution())
print('All Submissions Scheduled?', sol.EvaluateAllSubmissionsScheduled())
print('Is Solution Valid?', sol.ValidateSolution())
sol.printViolations()
sol.toExcel(file_name = 'New_Solution.xlsx')