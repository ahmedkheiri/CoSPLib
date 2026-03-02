# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.optimisation import *
from domain.problem import Problem
from solution import Solution

instance = "N2OR"
f_name = "Dataset/" + str(instance) + ".xlsx"

p = Problem(file_name=f_name)
parameters = p.build()
sol = Solution(p)

solver = ExactModel(p, sol)  # Available models: ExactModel(), ExtendedModel()
solver.solve(timelimit=3600)

print("Objective Value:", sol.EvaluateSolution())
print("All submissions scheduled? ", sol.EvaluateAllSubmissionsScheduled())
sol.printViolations()
sol.toExcel(file_name="Solution" + str(instance) + ".xlsx")
