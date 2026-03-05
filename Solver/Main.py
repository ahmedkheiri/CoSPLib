# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.algorithms.hyper_heuristic import HyperHeuristic
from optimisation.algorithms.matheuristic import Matheuristic
from domain.problem import Problem
from solution import Solution, RandomInd
from pathlib import Path
from time import time
import config
import logging


def solve_with_hyper_heuristic(problem: Problem) -> Solution:
    final_solution = RandomInd(problem)
    solver = HyperHeuristic()
    s_time = time()
    solver.solve(
        problem=problem,
        solution=final_solution,
        start_time=s_time,
        run_time_in_sec=3600,
        ruin_and_recreate_frequency_in_sec=600,
    )
    return final_solution


def solve_with_matheuristic(problem: Problem) -> Solution:
    final_solution = Solution(problem)
    solver = Matheuristic()
    s_time = time()
    solver.solve(
        problem=problem,
        solution=final_solution,
        start_time=s_time,
        run_time_in_sec=600,
        time_limit_in_sec=90,
        ruin_and_recreate_frequency_in_sec=600,
    )
    return final_solution


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    problem = Problem(file_path=Path(config.INPUT_PATH))
    problem.build()

    if config.HYPER_HEURISTIC:
        final_solution = solve_with_hyper_heuristic(problem)
    if config.MATHEURISTIC:
        final_solution = solve_with_matheuristic(problem)

    logging.info(
        f"Is solution feasible? {final_solution.EvaluateAllSubmissionsScheduled()}"
    )
    logging.info(f"Objective value: {final_solution.EvaluateSolution()}")
    final_solution.printViolations()

    """sol = Solution(problem)

    solver = ExactModel(problem, sol)  # Available models: ExactModel(), ExtendedModel()
    solver.solve(timelimit=3600)

    print("Objective Value:", sol.EvaluateSolution())
    print("All submissions scheduled? ", sol.EvaluateAllSubmissionsScheduled())
    sol.printViolations()
    sol.toExcel(file_name="Solution" + config.INSTANCE_NAME + ".xlsx")"""
