# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.algorithms.hyper_heuristic import HyperHeuristic
from domain.problem import Problem
from solution import Solution, RandomInd
from pathlib import Path
from time import time
import config
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    problem = Problem(file_path=Path(config.INPUT_PATH))
    problem.build()
    sol = RandomInd(problem)
    solver = HyperHeuristic()
    s_time = time()
    solver.solve(
        problem=problem,
        solution=sol,
        start_time=s_time,
        run_time_in_sec=60,
        ruin_and_recreate_frequency_in_sec=30,
    )
    print("Objective Value:", sol.EvaluateSolution())
    print("All submissions scheduled?", sol.EvaluateAllSubmissionsScheduled())
    sol.printViolations()
    """sol = Solution(problem)

    solver = ExactModel(problem, sol)  # Available models: ExactModel(), ExtendedModel()
    solver.solve(timelimit=3600)

    print("Objective Value:", sol.EvaluateSolution())
    print("All submissions scheduled? ", sol.EvaluateAllSubmissionsScheduled())
    sol.printViolations()
    sol.toExcel(file_name="Solution" + config.INSTANCE_NAME + ".xlsx")"""
