# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 20:15:13 2021

@author: pylya
"""

from Solution import *

############## MAIN ##############
p = Problem(file_name = "N2OR.xlsx")
parameters = p.ReadProblemInstance()
p.FindConflicts()
p.AssignTimezonesPenalties(parameters)
sol = Solution(p, parameters)
sol.ReadSolution(file_name = "Solution.xlsx")

print(sol.getSolTracks())
print(sol.getSolSubmissions())
print('Objective Value:', sol.EvaluateSolution())
print('All Submissions Scheduled?', sol.EvaluateAllSubmissionsScheduled())
print('Is Solution Valid?', sol.ValidateSolution())
sol.PrintViolations()
#sol.toExcel(file_name = 'Solution2.xlsx')
##################################
