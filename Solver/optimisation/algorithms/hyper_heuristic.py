"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from solution import Solution
from domain.problem import Problem
from typing import List
from optimisation.low_level_heuristics.swap_track import SwapTrack
from optimisation.low_level_heuristics.swap_submission import SwapSubmission
from optimisation.low_level_heuristics.reverse_submission import ReverseSubmission
from time import time
import numpy as np
import logging


class HyperHeuristic:
    def __init__(self) -> None:
        self.__low_level_heuristics: List[
            SwapTrack | SwapSubmission | ReverseSubmission
        ] = [SwapTrack(), SwapSubmission(), ReverseSubmission()]

    def solve(
        self,
        problem: Problem,
        solution: Solution,
        start_time: time,
        run_time_in_sec: int,
        ruin_and_recreate_frequency_in_sec: int = 600,
    ) -> None:
        logging.info("Solving with hyper-heuristic...")
        objective_best = solution.EvaluateSolution()
        objective_current = objective_best
        solution_best = solution.copyWholeSolution()
        iteration = 0
        s_time = time()
        next_ruin_and_recreate_time = ruin_and_recreate_frequency_in_sec
        while time() - start_time < run_time_in_sec:
            iteration += 1
            selected_llh = self.__low_level_heuristics[
                np.random.randint(len(self.__low_level_heuristics))
            ]
            solution_copy = solution.copyWholeSolution()
            selected_llh.apply(problem, solution)
            solution.resetSolSubmissions()
            solution.convertSol()
            if solution.EvaluateAllSubmissionsScheduled() == True:
                objective_new = solution.QuickEvaluateSolution(objective_current)
                if objective_new <= objective_current:
                    objective_current = objective_new
                    if objective_new < objective_best:
                        solution_best = solution.copyWholeSolution()
                        objective_best = objective_new
                        logging.info(f"Current best solution: {objective_best}")
                else:
                    solution.restoreSolution(
                        solution_copy[0], solution_copy[1], solution_copy[2]
                    )
            else:
                solution.restoreSolution(
                    solution_copy[0], solution_copy[1], solution_copy[2]
                )

            # Ruin & Recreate
            if time() - s_time > next_ruin_and_recreate_time:
                ruin_counter = 0
                while ruin_counter != 10:
                    solution_copy = solution.copyWholeSolution()
                    self.__low_level_heuristics[0].apply(problem, solution)
                    solution.resetSolSubmissions()
                    solution.convertSol()
                    if solution.EvaluateAllSubmissionsScheduled() == False:
                        solution.restoreSolution(
                            solution_copy[0], solution_copy[1], solution_copy[2]
                        )
                    else:
                        ruin_counter += 1
                objective_current = solution.EvaluateSolution()
                next_ruin_and_recreate_time += ruin_and_recreate_frequency_in_sec
        solution.setBestSolution(solution_best[0], solution_best[1])
        logging.info(f"Number of iterations {iteration}")
