"""
Created on Thu Mar 6 09:20:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.algorithms.hyper_heuristic import HyperHeuristic
from optimisation.algorithms.matheuristic import Matheuristic
from optimisation.milp.exact_model import ExactModel
from optimisation.milp.extended_model import ExtendedModel
from domain.problem import Problem
from solution import Solution, RandomIndirectSolution
from time import time
import config


def solve_with_hyper_heuristic(problem: Problem) -> Solution:
    final_solution = RandomIndirectSolution(problem)
    solver = HyperHeuristic()
    s_time = time()
    solver.solve(
        problem=problem,
        solution=final_solution,
        start_time=s_time,
        run_time_in_sec=config.TIME_LIMIT_IN_SEC,
        ruin_and_recreate_frequency_in_sec=config.RUIN_AND_RECREATE_TIME_FREQUENCY_IN_SEC,
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
        run_time_in_sec=config.TIME_LIMIT_IN_SEC,
        milp_time_limit_in_sec=config.MILP_TIME_LIMIT_IN_SEC,
        ruin_and_recreate_frequency_in_sec=config.RUIN_AND_RECREATE_TIME_FREQUENCY_IN_SEC,
    )
    return final_solution


def solve_with_exact_milp(problem: Problem) -> Solution:
    final_solution = Solution(problem)
    solver = ExactModel(problem, final_solution)
    solver.solve(time_limit_in_sec=config.TIME_LIMIT_IN_SEC)
    return final_solution


def solve_with_extended_milp(problem: Problem) -> Solution:
    final_solution = Solution(problem)
    solver = ExtendedModel(problem, final_solution)
    solver.solve(time_limit_in_sec=config.TIME_LIMIT_IN_SEC)
    return final_solution
