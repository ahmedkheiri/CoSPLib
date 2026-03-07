"""
Created on Thu Mar 5 11:11:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from time import time
from optimisation.milp.tracks_exact_model import TracksExactModel
from optimisation.algorithms.hyper_heuristic import HyperHeuristic
from domain.problem import Problem
from solution import Solution


class Matheuristic:
    def solve(
        self,
        problem: Problem,
        solution: Solution,
        start_time: time,
        run_time_in_sec: int,
        time_limit_in_sec=90,
        ruin_and_recreate_frequency_in_sec=600,
    ) -> None:
        milp_model = TracksExactModel(problem, solution)
        milp_model.solve(time_limit_in_sec)
        solution.convert_indirect_solution_first_time()
        hyper_heuristic = HyperHeuristic()
        hyper_heuristic.solve(
            problem,
            solution,
            start_time,
            run_time_in_sec,
            ruin_and_recreate_frequency_in_sec,
        )
